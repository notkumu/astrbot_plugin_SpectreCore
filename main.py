import os
import traceback
import time
from astrbot.api.all import *
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from .message_processor import MessageProcessor
from .message_formatter import MessageFormatter
from .utils.chat_formatter import format_chat_history
from .utils.reply_decision import should_reply
from .utils.persona_handler import get_persona_info
from .utils.text_filter import filter_thinking_process

@register(
    "spectrecore",
    "23q3", 
    "使大模型更好的主动回复群聊中的消息，带来生动和沉浸的群聊对话体验",
    "1.0.0",
    "https://github.com/23q3/astrbot_plugin_SpectreCore"
)
class SpectreCore(Star):
    """SpectreCore插件主类
    
    负责接收群消息事件，并调用消息处理器处理消息
    """
    
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.base_path = os.path.join("data", "group_messages")
        os.makedirs(self.base_path, exist_ok=True)
        logger.info(f"SpectreCore插件初始化完成，消息存储路径: {self.base_path}")

    async def get_group_message_history(self, client, group_id):
        """获取群消息历史"""
        try:
            response = await client.api.call_action(
                "get_group_msg_history",
                group_id=group_id,
                count=self.config.get('group_msg_history', 20)
            )
            logger.debug(f"获取群 {group_id} 消息历史成功")
            return response
        except Exception as e:
            logger.error(f"获取群 {group_id} 消息历史失败: {str(e)}")
            return None

    async def collect_image_urls(self, messages, latest_message_index, img_count):
        """收集图片URL"""
        if img_count <= 0:
            return []
            
        image_urls = []
        latest_message = messages[latest_message_index]
        
        # 从最新消息中收集图片
        for seg in latest_message.get('message', []):
            if seg.get('type') == 'image':
                url = seg.get('data', {}).get('url')
                if url:
                    image_urls.append(url)
        
        # 如果需要更多图片，从其他消息中收集
        if len(image_urls) < img_count:
            for msg in messages[:latest_message_index]:
                if len(image_urls) >= img_count:
                    break
                for seg in msg.get('message', []):
                    if seg.get('type') == 'image':
                        url = seg.get('data', {}).get('url')
                        if url and url not in image_urls:
                            image_urls.append(url)
                            if len(image_urls) >= img_count:
                                break
        
        return image_urls[:img_count]

    async def prepare_model_prompt(self, persona_info):
        """准备模型系统提示词和上下文"""
        system_prompt = f"当前时间:{time.strftime('%Y-%m-%d %H:%M:%S')}"
        contexts = []
        
        if persona_info:
            # 添加人格提示词
            if persona_info.get('prompt'):
                system_prompt += f"\n\n{persona_info.get('prompt')}"
            
            # 添加对话风格模仿提示
            mood_imitation = persona_info.get('_mood_imitation_dialogs_processed')
            if mood_imitation:
                system_prompt += f"\n\n请模仿以下对话风格进行回复：\n{mood_imitation}"
            
            # 添加预设对话上下文
            begin_dialogs = persona_info.get('_begin_dialogs_processed', [])
            if begin_dialogs:
                contexts.extend(begin_dialogs)
        
        return system_prompt, contexts
        
    def process_model_response(self, reply_text: str) -> str:
        """
        处理模型的回复内容，根据配置进行文本过滤
        
        Args:
            reply_text: 模型原始回复文本
            
        Returns:
            处理后的回复文本
        """
        # 如果回复为空，直接返回
        if not reply_text:
            self.logger.warning("收到空回复")
            return reply_text
        
        # 检查是否需要过滤思考过程
        filter_thinking = self.config.get('filter_thinking', True)
        
        if filter_thinking:
            # 检查文本开头是否包含思考标签
            if reply_text.startswith('<think>'):
                logger.info("检测到思考过程，正在过滤...")
                filtered_text = filter_thinking_process(reply_text)
                return filtered_text
            else:
                # 没有思考内容需要过滤
                return reply_text
        else:
            # 不启用过滤
            logger.debug("思考过程过滤已禁用")
            return reply_text

    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """处理群消息事件"""
        try:
            # 检查事件类型
            if not isinstance(event, AiocqhttpMessageEvent):
                logger.debug("非AiocqhttpMessageEvent类型的消息，跳过处理")
                return
                
            client = event.bot
            group_id = event.get_group_id()
            
            # 获取群消息历史
            response = await self.get_group_message_history(client, group_id)
            if not response or 'messages' not in response or not response['messages']:
                return
                
            messages = response['messages']
            
            # 处理并保存消息
            save_result = await MessageProcessor.save_messages(
                group_id, messages, self.base_path, client
            )
            
            if not save_result:
                logger.warning(f"群 {group_id} 的消息保存失败")
                return

            # 获取当前消息内容，决定是否回复
            latest_message_index = len(messages) - 1
            latest_message = messages[latest_message_index]
            
            current_message = await MessageFormatter.process_group_message(
                latest_message, messages, client, group_id
            )
            content = current_message.get('content', '')
            
            # 判断是否需要回复
            if not should_reply(content, self.config, group_id):
                return
                
            # 准备调用大模型
            chat_history = await format_chat_history(group_id, self.base_path, self.config)
            prompt = f"你在一个qq群聊中，以下是群聊的聊天记录:\n{chat_history}\n\n现在轮到你回复了，请直接输出你要发送的消息，不要输出任何解释，你只能回复普通的文本，不能回复如[qq表情:生气]或@某人等特殊内容"
            
            # 收集图片URL
            img_count = self.config.get('image_count', 0)
            image_urls = await self.collect_image_urls(messages, latest_message_index, img_count)
            
            # 获取人格信息
            persona_name = self.config.get('persona', '')
            persona_info = await get_persona_info(persona_name, self.context)
            
            # 准备系统提示词和上下文
            system_prompt, contexts = await self.prepare_model_prompt(persona_info)
            logger.debug(f"提示词: {prompt}")
            # 调用大模型
            func_tools_mgr = self.context.get_llm_tool_manager()
            llm_response = await self.context.get_using_provider().text_chat(
                prompt=prompt,
                contexts=contexts,
                image_urls=image_urls,
                func_tool=func_tools_mgr,
                system_prompt=system_prompt
            )
  
            
            # 发送回复
            if llm_response.role == "assistant":
                # 处理回复文本，过滤思考过程
                response_text = self.process_model_response(llm_response.completion_text)
                logger.info(f"大模型回复: {response_text[:100]}...")
                yield event.plain_result(response_text)
            elif llm_response.role == "tool":
                tool_response = f"工具调用: {llm_response.tools_call_name}, 参数: {llm_response.tools_call_args}"
                logger.info(tool_response)

        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"处理群消息时出错: {str(e)}\n{error_details}")