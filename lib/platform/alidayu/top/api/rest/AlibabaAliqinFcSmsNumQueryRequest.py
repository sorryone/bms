'''
Created by auto_sdk on 2015.12.18
'''
from top.api.base import RestApi
class AlibabaAliqinFcSmsNumQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.biz_id = None
		self.current_page = None
		self.page_size = None
		self.query_date = None
		self.rec_num = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.sms.num.query'
