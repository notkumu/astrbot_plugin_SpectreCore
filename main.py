import os
import json
from datetime import datetime
from typing import Tuple
from astrbot.api.all import *

@register(
    "spectrecore",
    "23q3", 
    "使大模型更好的主动回复群聊中的消息，带来生动和沉浸的群聊对话体验",
    "1.0.0",
    "https://github.com/23q3/astrbot_plugin_SpectreCore"
)
class SpectreCore(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 设置消息存储目录
        self.base_path = os.path.join("data", "group_messages")
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def find_message_by_id(self, group_id: str, message_id: str) -> dict:
        #根据消息ID查找历史消息
        file_path = os.path.join(self.base_path, f"group_{group_id}.json")
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)
                for msg in messages:
                    if msg.get("message_id") == message_id:
                        return msg
        except Exception as e:
            logger.error(f"查询历史消息失败: {str(e)}")
        return None

    def process_message(self, message_obj, group_id: str) -> Tuple[str, str, str]:
        # 处理消息内容,将不同类型的消息格式化为统一格式       
        # 初始化返回值
        message = ""
        msg_type = "text" 
        url = ""
        
        # 解析消息数据
        for msg in message_obj.raw_message.message:
            curr_type = msg.get('type', '')
            data = msg.get('data', {})
            
            # 根据消息类型分别处理
            if curr_type == 'reply':
                # 处理回复消息
                replied_id = data.get('id', '')
                # 查找被回复的消息
                replied_msg = self.find_message_by_id(group_id, replied_id)
                
                if replied_msg:
                    # 找到原消息，使用完整格式
                    message += f"[回复{replied_msg['user_name']} id:{replied_msg['user_id']}的消息:{replied_msg['message']}]"
                else:
                    # 未找到原消息，使用简略格式
                    message += f"[回复id:{replied_id}的消息]"
                msg_type = 'text'
                
            elif curr_type == 'text':
                # 处理文本消息
                message += data.get('text', '')
                msg_type = 'text'
            
            elif curr_type == 'face':
                # 处理表情,优先使用表情描述文本
                raw = data.get('raw', {})
                face_text = raw.get('faceText', '')
                message = f"[表情:{face_text}]" if face_text else f"[表情:{data.get('id', '')}]"
                msg_type = 'face'
            
            elif curr_type == 'at':
                # 处理@消息
                qq = data.get('qq', '未知')
                message = f"[@{qq}]"
                msg_type = 'at'
            
            elif curr_type == 'image':
                # 处理图片消息,保存URL
                message = "[图片]"
                url = data.get('url', '')
                msg_type = 'image'
            
            elif curr_type == 'dice':
                # 处理骰子消息
                result = data.get('result', '?')
                message = f"[骰子:{result}点]"
                msg_type = 'dice'
            
            elif curr_type == 'rps':
                # 处理猜拳消息
                result = data.get('result', '?')
                rps_text = {
                    '1': '布',
                    '2': '剪刀', 
                    '3': '石头'
                }.get(str(result), '未知')
                message = f"[猜拳:{rps_text}]"
                msg_type = 'rps'
            else:
                # 处理未知类型的消息
                message = "[未知消息类型]"
                msg_type = 'unknown'
                
        return message.strip(), msg_type, url

    def save_messages(self, file_path: str, msg_data: dict) -> None:
        # 保存消息到JSON文件
        messages = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    messages = json.load(f)
            except json.JSONDecodeError:
                messages = []
        
        messages.append(msg_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent) -> None:
        '''监听并记录群聊消息'''
        try:
            # 获取消息基本信息
            group_id = event.message_obj.group_id
            sender_name = event.get_sender_name()
            sender_id = event.get_sender_id()
            timestamp = event.message_obj.timestamp
            
            # 添加消息ID
            message_id = str(event.message_obj.message_id)
            
            # 处理消息内容，传入group_id用于查询历史消息
            message, msg_type, url = self.process_message(event.message_obj, str(group_id))
            
            # 构建消息数据结构
            msg_data = {
                "time": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"),
                "user_name": sender_name,
                "user_id": sender_id,
                "message": message,
                "type": msg_type,
                "url": url,
                "message_id": message_id  
            }
            
            # 记录日志
            logger.info(f"存储消息数据: {msg_data}")
            
            # 保存到文件
            file_path = os.path.join(self.base_path, f"group_{group_id}.json")
            self.save_messages(file_path, msg_data)
                
        except Exception as e:
            logger.error(f"存储群消息失败: {str(e)}")
            logger.exception(e)