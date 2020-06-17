import time
import copy
import datetime
import json
import threading
import sys
import redis
import cv2

import subprocess as sp
from os import path
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from decimal import Decimal

from ws_server import ws

redi_cli = redis.Redis(host='localhost', port=6379, decode_responses=True)

# big 544x960
# live 640x1114
# 阿里云的live地址
# live_url = 'rtmp://live.blueholetech.com/human/guizhou?auth_key=1591127408-0-0-70ec74ed845ff0c3f214da330e00c20d'
# 自定义
live_url = 'rtmp://47.103.119.180/live'
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', '640x1114',
           '-r', '1',
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           live_url]

print(command)

p = sp.Popen(command, stdin=sp.PIPE)


class Command(BaseCommand):
    args = ""

    def handle(self, *args, **options):
        self.last_frame = ''

        self.run()

    def run(self):
        while True:
            cache_key = 'video_queue'
            file_path = redi_cli.lpop(cache_key)
            if not file_path:
                if self.last_frame:
                    # print('推最后一帧。。。', len(last_frame))
                    p.stdin.write(self.last_frame)
                continue

            if redi_cli.llen(cache_key) >= 2:
                print('跳帧......', redi_cli.llen(cache_key))
                continue

            cap = cv2.VideoCapture(file_path)

            print("读取到新文件:", file_path, "队列长度:", redi_cli.llen(cache_key))

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    # print("Opening camera is failed")
                    break

                last_frame = copy.copy(frame.tostring())
                p.stdin.write(last_frame)
