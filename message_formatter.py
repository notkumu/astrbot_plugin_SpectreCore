from typing import Dict, List
import time
import asyncio
import json
from astrbot.api.all import logger
from .processors.segment_processor import SegmentProcessor
from .processors.image_processor import ImageProcessor
from .cache import name_cache

class MessageFormatter:
    """消息格式化类，负责将原始消息处理成结构化数据"""
    
    @classmethod
    async def process_group_message(cls, message_data: Dict, messages: List[Dict] = None, client = None, group_id: int = None) -> Dict:
        """处理群消息，返回格式化后的消息字典"""
        message = message_data['message']
        sender = message_data['sender']
        message_time = message_data['time']
        
        # 缓存用户信息
        name_cache.put(str(sender['user_id']), sender['nickname'])
        
        # 检查特殊消息类型
        special_message = await cls._check_special_message_types(message, sender, message_time)
        if special_message:
            return special_message

        # 处理普通消息
        return await cls._process_normal_message(message_data, messages, client, group_id)
        
    @classmethod
    async def _check_special_message_types(cls, message: List[Dict], sender: Dict, message_time: int) -> Dict:
        """检查是否为特殊类型的消息，如合并转发消息"""
        for seg in message:
            # 处理常规合并转发消息
            if seg['type'] == 'forward':
                from .processors.forward_processor import ForwardProcessor
                logger.debug(f"检测到合并转发消息，发送者：{sender['nickname']}，时间：{message_time}")
                return await ForwardProcessor.process_forward_message(
                    seg['data'], 
                    sender_info=sender,
                    msg_time=message_time
                )
            
            # 处理伪合并转发消息
            if seg['type'] == 'json':
                processed_message = await cls._process_pseudo_forward(seg, sender, message_time)
                if processed_message:
                    return processed_message
                    
        return None
        
    @classmethod
    async def _process_pseudo_forward(cls, segment: Dict, sender: Dict, message_time: int) -> Dict:
        """处理伪合并转发消息"""
        try:
            json_data = json.loads(segment['data']['data'])
            if json_data.get('app') == 'com.tencent.multimsg':
                logger.debug(f"检测到伪合并转发消息，发送者：{sender['nickname']}，时间：{message_time}")
                from .processors.forward_processor import ForwardProcessor
                
                # 构建伪合并转发消息数据
                pseudo_forward_data = {'content': []}
                
                # 提取消息内容
                news_items = json_data.get('meta', {}).get('detail', {}).get('news', [])
                for item in news_items:
                    if 'text' in item:
                        pseudo_forward_data['content'].append({
                            'time': message_time,
                            'sender': sender,
                            'message': [{'type': 'text', 'data': {'text': item['text']}}]
                        })
                
                return await ForwardProcessor.process_forward_message(
                    pseudo_forward_data,
                    sender_info=sender,
                    msg_time=message_time
                )
        except Exception as e:
            logger.error(f"处理伪合并转发消息时出错: {str(e)}", exc_info=True)
            
        return None
        
    @classmethod
    async def _process_normal_message(cls, message_data: Dict, messages: List[Dict] = None, client = None, group_id: int = None) -> Dict:
        """处理普通消息"""
        message = message_data['message']
        sender = message_data['sender']
        
        # 批量处理消息段落
        tasks = [SegmentProcessor.process_message_segment(seg, messages, client, group_id) for seg in message]
        processed_segments = await asyncio.gather(*tasks)
        
        # 构建结果字典
        result = {
            'time': time.strftime('%Y-%m-%d %H:%M:%S', 
                                time.localtime(message_data['time'])),
            'sender': f"{sender['nickname']}(id:{sender['user_id']})",
            'content': ''.join(processed_segments),
            'resources': []
        }

        # 收集资源信息
        for seg in message:
            if seg['type'] == 'image':
                image_info = ImageProcessor.process_image_data(seg['data'])
                result['resources'].append(image_info)

        return result 