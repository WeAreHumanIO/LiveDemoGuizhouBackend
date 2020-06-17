import redis
import sys
import subprocess

redi_cli = redis.Redis(host='localhost', port=6379, decode_responses=True)
stream_path = '/wearehuman/wechat_fun_api/media/stream/%s'
mp4_path = '/wearehuman/wechat_fun_api/media/stream/mp4/%s.mp4'


def set_redis(filename):
    # _file_name = filename.split('.')[0]
    # source = stream_path % filename
    # mp4_source = mp4_path % _file_name
    # cmd = "ffmpeg -y -i  %s -vcodec copy -acodec copy %s" % (source, mp4_source)
    # subprocess.call([cmd], shell=True)

    redi_cli.lpush('liuxin_live', filename)


if __name__ == "__main__":
    set_redis(sys.argv[1])
