from typing import Dict, List
import json
import os
import aiofiles
import asyncio
import time
from astrbot.api.all import logger

from .message_formatter import MessageFormatter

class MessageProcessor:
    """消息处理器，用于处理和保存QQ群消息"""
    
    @classmethod
    async def save_messages(cls, group_id: int, messages: List[Dict], base_path: str, client = None):
        """异步保存消息到JSON文件"""
        try:
            file_path = os.path.join(base_path, f"{group_id}.json")
            
            # 使用异步并发处理所有消息
            tasks = [MessageFormatter.process_group_message(msg, messages, client, group_id) for msg in messages]
            processed_messages = await asyncio.gather(*tasks)
            
            json_data = {
                "group_id": group_id,
                "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "messages": processed_messages
            }
            
            # 使用临时文件写入再重命名，避免写入中断导致文件损坏
            temp_file = f"{file_path}.tmp"
            async with aiofiles.open(temp_file, 'w', encoding='utf-8') as f:
                await f.write(
                    json.dumps(
                        json_data,
                        ensure_ascii=False,
                        indent=2
                    )
                )
            
            # Windows下可能需要先删除目标文件
            if os.path.exists(file_path):
                os.remove(file_path)
                
            os.rename(temp_file, file_path)
            logger.debug(f"成功保存群 {group_id} 的消息，共 {len(processed_messages)} 条")
            return True
            
        except Exception as e:
            logger.error(f"保存消息时出错: {str(e)}", exc_info=True)
            return False
