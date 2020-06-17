# import time
# import datetime
# import json
# import threading
# import sys
# import redis
# 
# from os import path
# from django.conf import settings
# from django.core.management import BaseCommand
# from django.db import transaction
# from decimal import Decimal
# 
# from ws_server import ws
# 
# # 外部导入
# sys.path.append(path.abspath('/opt/core/VideoProcessor/processor'))
# import emonet
# from process_core.emonet.application import emotion_detector
# from process_core.process import delayed_video_processing
# 
# # ED = emonet.application.Emotion_Detector(verbose=0, bbox_minsize=0.05)
# ED = emotion_detector(
#     order_faces='size',
#     nb_faces=1,
#     max_res=640,
#     bbox_minsize=0.3,
#     fps=1
# )
# 
# redi_cli = redis.Redis(host='localhost', port=6379, decode_responses=True)
# 
# """
# import cv2
# v = cv2.VideoCapture('rtmp://live.blueholetech.com/human/guizhou?auth_key=1591133046-0-0-023b6de2b5a97166c655079cdeb87ad5')
# v.isOpened()
# rval, frame = v.read()
# cv2.imwrite('/home/test.jpg', frame)
# 
# https://blog.csdn.net/qq_38214193/article/details/80997924
# """
# 
# 
# class Command(BaseCommand):
#     args = ""
# 
#     def handle(self, *args, **options):
#         self.run()
# 
#     def run(self):
# 
# 
# video_path = 'rtmp://live.blueholetech.com/human/guizhou?auth_key=1591650244-0-0-c8b395e5a2c26c4004d4e1aeac8bf39d'
# video = cv2.VideoCapture()
# if not video.open(video_path):
#     print("can not open the video")
#     exit(1)
# 
# while True:
#     _, frame = video.read()
#     if frame is None:
#         print('当前没有直播了.')
#         break
#     cv2.imwrite('%s.jpg' % int(time.time()), frame)
# 
#     v = cv2.VideoCapture(
#         'rtmp://live.blueholetech.com/human/guizhou?auth_key=1591650244-0-0-c8b395e5a2c26c4004d4e1aeac8bf39d')
#     v.isOpened()
#     rval, frame = v.read()
#     cv2.imwrite('%s.jpg' % int(time.time()), frame)
# 
#             video_path = '/wearehuman/wechat_fun_api/media/stream/%s' % file_name
#             start_time = int(time.time())
#             _file_name = file_name.split('.flv')[0]
#             path_tmp = '/tmp/%s' % _file_name
#             print('开始处理....', video_path)
#             ED.run(video_path, path_tmp)
#             export_video = '/opt/core/VideoProcessor/processor/result/video_processed/%s.mp4' % _file_name
# 
#             # 导出mp4视频文件
#             ED.export(path_tmp, export_video)
#             redi_cli.lpush('video_queue', export_video)
#             res_all, res_avr = ED.get_summary(path_tmp)
# 
#             print(file_name, '分析完成:')
#             print("处理时间:", time.time() - start_time, "剩余待处理长度:", redi_cli.llen(cache_key))
#             print("res_all：", res_all)
#             print("res_avr：", res_avr)
# 
#             ws.push(res_all)
