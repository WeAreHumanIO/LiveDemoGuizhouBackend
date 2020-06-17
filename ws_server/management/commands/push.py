import time
import datetime
import base64
import json
import threading
import sys
import redis
import pickle
import tensorflow as tf

from os import path
from decimal import Decimal
from django.core.management import BaseCommand

from ws_server import ws
from ws_server.ws import GROUP_NAME

# 外部导入 Dayee
sys.path.append(path.abspath('/opt/core/VideoProcessor/processor/process_core'))
from emonet.application import emotion_detector

ED = emotion_detector(
    order_faces='size',
    nb_faces=-1,
    max_res=640,
    bbox_minsize=0.15,
    fps=1
)

redis_cli = redis.Redis(host='localhost', port=6379, decode_responses=True)

print('初始化成功....')


class Command(BaseCommand):
    args = ""

    def handle(self, *args, **options):
        self.run()

    def calculate(self, user_key, data):
        user_key = '%s3' % user_key
        data = list(data)
        if len(data) <= 1:
            return data

        if not data[1]:
            return data

        frame = {}
        personality_data = {}
        cache_data = redis_cli.get(user_key)
        if cache_data:
            frame, personality_data = json.loads(cache_data)

        for k, v in data[1].items():
            if k not in personality_data:
                personality_data[k] = {'personality_data': {}}
            if k not in frame:
                frame[k] = 0
            frame[k] += 1
            print("frame:", frame)
            for item_key, item_value in v['personality_data'].items():
                if item_key not in personality_data[k]['personality_data']:
                    personality_data[k]['personality_data'][item_key] = 0

                print(item_key, personality_data[k]['personality_data'][item_key], 'now:', item_value)
                personality_data[k]['personality_data'][item_key] += item_value

        # 累加完后先存储起来
        redis_cli.set(user_key, json.dumps([frame, personality_data]))
        print("累加后:", personality_data['0']['personality_data']['anger'])

        # 计算平均分
        for k, v in personality_data.items():
            frame_item = frame.get(k, 1)
            for item_k in v['personality_data'].keys():
                v['personality_data'][item_k] /= frame_item

        print("计算后:", frame, personality_data['0']['personality_data']['anger'])

        data[1] = personality_data
        return tuple(data)

    def main(self):
        data = redis_cli.lpop(GROUP_NAME)
        if not data: return

        push_key, base_data = data.split('#######')

        if redis_cli.llen(GROUP_NAME) >= 2:
            print('跳帧......', redis_cli.llen(GROUP_NAME))
            return

        timestamp = int(time.time())
        image_data = base64.b64decode(base_data)
        image_path = '/tmp/save_images/%s.jpg' % timestamp
        file = open(image_path, "wb")
        file.write(image_data)
        file.close()

        start_time = time.time()
        tmp_path = '/tmp/%s' % timestamp
        ED.run(image_path, tmp_path)
        data = ED.get_summary(tmp_path)
        # print(data)
        print('耗时:', time.time() - start_time)
        print("push_key:", push_key)

        data = self.calculate(push_key, data)
        print("xxxxx" * 33, data)

        ws.push(data, push_key=push_key)

    def run(self):
        while True:
            try:
                self.main()
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
