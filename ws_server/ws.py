import os
import time
import json
import base64
import cv2
import redis
import sys
import pickle
import numpy as np
import tensorflow as tf

from os import path
from asgiref.sync import async_to_sync
from django.db import connection
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer

GROUP_NAME = 'WEB_SOCKET_GUIZHOU'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
redis_cli = redis.Redis(host='localhost', port=6379, decode_responses=True)


class WebSocketServer(AsyncWebsocketConsumer):
    async def connect(self):  # 连接时触发
        self.ws_cache_key = GROUP_NAME

        query_string = self.scope.get('query_string')
        print("xxxxx" * 33, query_string)

        token = None
        if query_string and 'token=' in str(query_string):
            query_string = query_string.decode()
            token = query_string.split('token=')[1]
            print('token:', token)

        if token:
            self.ws_cache_key = token

        # 将新的连接加入到对应的拍卖场
        await self.channel_layer.group_add(
            self.ws_cache_key,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 将关闭的连接从拍卖场中移除
        print("断开连接")
        await self.channel_layer.group_discard(
            self.ws_cache_key,
            self.channel_name
        )
        connection.close()

    async def receive(self, text_data=None, bytes_data=None):
        """只用作测试push"""
        if text_data and not bytes_data:
            bytes_data = text_data

        data = self.ws_cache_key + "#######%s" % bytes_data
        redis_cli.lpush(GROUP_NAME, data)
        print('新到数据.....')

    async def system_message(self, event):
        message = event['data']

        # Send message to WebSocket单发消息
        await self.send(text_data=event['data'])


def push(data, push_key=GROUP_NAME):
    """
    从浏览器端push消息
    >>> from auction_house import ws
    >>> ws.push({'key': 'game_time', 'value': 100})
    >>> ws.push({'key': 'game_time', 'value': 100})
    """
    channel_layer = get_channel_layer()
    # ws_cache_key = GROUP_NAME % auction_house_id

    async_to_sync(channel_layer.group_send)(
        push_key,
        {
            "type": 'system_message',
            'data': json.dumps(data),
        }
    )
