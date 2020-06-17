# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.request import CommonRequest
# client = AcsClient('LTAI4FfYu56vELH5PXS93X2p', '5tSedeVihkIEBg2vPXmIBrSQefNU6f', 'cn-hangzhou')
#
# request = CommonRequest()
# request.set_accept_format('json')
# request.set_domain('rtc.aliyuncs.com')
# request.set_method('POST')
# request.set_protocol_type('http') # https | http
# request.set_version('2018-01-11')
# request.set_action_name('StartMPUTask')
#
# request.add_query_param('RegionId', "cn-hangzhou")
# request.add_query_param('ChannelId', "111")
# request.add_query_param('TaskId', "guizhou_server_task")
# request.add_query_param('MediaEncode', "1")
# request.add_query_param('LayoutIds.1', "1")
# request.add_query_param('StreamURL', "rtmp://47.103.119.180/live")
# request.add_query_param('AppId', "elyd2946")
#
# response = client.do_action(request)
# # python2:  print(response)
# print(str(response, encoding = 'utf-8'))