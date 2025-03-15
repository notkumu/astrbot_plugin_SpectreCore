from typing import Dict
from astrbot.api.all import logger
from .cache import name_cache, message_cache

class APIClient:
    """API调用的封装"""
    
    @classmethod
    async def get_group_member_info(cls, client, group_id: int, user_id: str) -> str:
        """通过API获取群成员信息"""
        try:
            response = await client.api.call_action(
                "get_group_member_info",
                group_id=group_id,
                user_id=user_id
            )
            
            if isinstance(response, dict):
                # 优先使用群名片,没有则使用昵称
                name = response.get('card') or response.get('nickname')
                if name:
                    # 同时缓存用户信息
                    name_cache.put(user_id, name)
                    return name
                return ''
            return ''
        except Exception as e:
            logger.error(f"获取群成员信息失败: {e}")
            return ''
    
    @classmethod
    async def get_message_by_id(cls, client, message_id: str) -> Dict:
        """通过API获取消息"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.debug(f"尝试通过API获取消息({attempt+1}/{max_retries}): {message_id}")
                response = await client.api.call_action(
                    "get_msg",
                    message_id=int(message_id)
                )
                logger.debug(f"API返回结果: {response}")
                if isinstance(response, dict):
                    message_cache.put(str(message_id), response, expire=300)  # 缓存5分钟
                    return response
                return {}
            except aiohttp.ServerDisconnectedError as e:
                logger.warning(f"服务器连接断开，正在重试({attempt+1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    logger.error(f"获取消息最终失败: {message_id}")
                    message_cache.put(str(message_id), {}, expire=60)  # 空缓存1分钟
                    return {}
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"获取消息失败, ID: {message_id}, 错误类型: {type(e).__name__}, 详情: {e}")
                message_cache.put(str(message_id), {}, expire=60)
                return {}
        
    @classmethod
    async def get_group_message_history(cls, client, group_id, count=20):
        """获取群消息历史"""
        try:
            response = await client.api.call_action(
                "get_group_msg_history",
                group_id=group_id,
                count=count
            )
            logger.debug(f"获取群 {group_id} 消息历史成功")
            return response
        except Exception as e:
            logger.error(f"获取群 {group_id} 消息历史失败: {str(e)}")
            return None 
    @classmethod
    async def get_login_info(cls, client) -> list:
        """获取登录号信息"""
        try:
            response = await client.api.call_action("get_login_info")
            return response           
        except Exception as e:
            logger.error(f"获取登录号信息失败: {str(e)}")
            return None

