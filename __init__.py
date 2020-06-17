# 推流地址: rtmp://47.103.119.180/push
# 播放地址: rtmp://47.103.119.180/live
# ws连接地址: ws://47.103.119.180:3333/ws/accept/
# wss连接地址: wss://ws.wearehuman.cn/ws/accept/


# nohup /opt/core/VideoProcessor/video/bin/python manage_local.py runserver 0.0.0.0:3333
# nohup /opt/core/VideoProcessor/video/bin/daphne -b 0.0.0.0 -p 3335 asgi:application&