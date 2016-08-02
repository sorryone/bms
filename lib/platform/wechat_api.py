# -*- coding: utf-8 -*-
import time
import datetime
import urllib
import requests
import string
import random
import hashlib
import xml.etree.ElementTree as ET
from django.conf import settings
from wechatpy.utils import check_signature
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.pay import WeChatPay
from wechatpy import WeChatClient
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
from wechatpy.replies import VoiceReply
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from lib.redis_model import StringModel
from lib.platform import wechat_const as const

# http://wechatpy.readthedocs.io/zh_CN/latest/quickstart.html
WECHAT_APPID = "wx8bbf0161ef2a6209"
WECHAT_AESKEY = "9lGuZLFVQw795105VstFopGQ1C7gaIPJTPdOsLX8FLM"
WECHAT_TOKEN = "bellcatwechat"
WECHAT_APPSECRET = "e1a57fd88bc1f94f5ffd2520add1beb9"
WECHAT_GET_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token?%s"


class WECHAT_TOKEN(StringModel):
    pass


class WECHATAPI(object):
    def __init__(self):
        self.app_id = settings.WECHAT_APPID
        self.aes_key = settings.WECHAT_AESKEY
        self.token = settings.WECHAT_TOKEN
        self.app_secret = settings.WECHAT_APPSECRET
        self.mch_id = settings.WECHAT_MCHID
        self.pay_key = settings.WECHAT_PAYKEY
        self.client = WeChatClient(self.app_id, self.app_secret)
        self.pay = WeChatPay(self.app_id, self.pay_key, self.mch_id)

    def _get_sign(self, data):
        # 第一步：对参数按照key=value的格式，并按照参数名ASCII字典序排序如下：
        d_str = self._format_dict(data)
        # 第二步：拼接API密钥：
        d_str = "{0}&key={1}".format(d_str, self.pay_key)
        # 第三步：加密转大写
        d_str = hashlib.md5(d_str).hexdigest()
        result = d_str.upper()
        return result

    def _format_dict(self, data, urlencode=False):
        slist = sorted(data)
        buff = []
        for k in slist:
            v = urllib.quote(data[k]) if urlencode else data[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def _xmltodict(self, xml):
        data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            data[child.tag] = value
        return data

    def _dicttoxml(self, data):
        xml = ["<xml>"]
        for k, v in data.iteritems():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))

        xml.append("</xml>")
        return "".join(xml)

    def _random_str(self, randomlength=32):
        a = list(string.ascii_letters + "1234567890")
        random.shuffle(a)
        return ''.join(a[:randomlength])

    def create_QRCode(self, product_id):
        data = {
            "product_id": str(product_id),
            "appid": self.app_id,
            "mch_id": self.mch_id,
            "time_stamp": str(int(time.time())),
            "nonce_str": self._random_str(),
        }
        sign = self._get_sign(data)
        data["sign"] = sign
        params = self._format_dict(data)
        url = "weixin://wxpay/bizpayurl?" + params
        short_url = self.client.misc.short_url(url)
        if short_url.get("short_url"):
            url = short_url["short_url"]
        return url, self._dicttoxml(data)

    def check_wechat(self, signature, timestamp, nonce):
        try:
            check_signature(self.token, signature, timestamp, nonce)
        except InvalidSignatureException:
            return False

        return True

    def create_order(self, data):
        """
            body(128), total_fee, product_id, detail(8192)
        """
        if "detail" in data:
            if len(data["detail"]) > 8192:
                return False

        if "body" in data:
            if len(data["body"]) > 128:
                return False

        if "total_fee" not in data:
            return False

        if "product_id" not in data:
            return False

        base_data = {
            # – 交易类型，取值如下：JSAPI，NATIVE，APP，WAP
            "trade_type": "NATIVE",
            # – 商品描述
            "body": "BellcatGame",
            # – 总金额，单位分
            "total_fee": "1",
            # – 接收微信支付异步通知回调地址
            "notify_url": settings.SERVER_ROOT + "/bms/pay_callback/",
            # – 可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
            "client_ip": settings.SERVER_IP,
            # – 可选，用户在商户appid下的唯一标识。trade_type=JSAPI，此参数必传
            "user_id": "",
            # – 可选，商户订单号，默认自动生成
            "out_trade_no": "",
            # – 可选，商品详情
            "detail": "",
            # – 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
            "attach": "",
            # – 可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
            "fee_type": "",
            # – 可选，订单生成时间，默认为当前时间
            "time_start": datetime.datetime.now(),
            # – 可选，订单失效时间，默认为订单生成时间后两小时
            # "time_expire": "",
            # – 可选，商品标记，代金券或立减优惠功能的参数
            "goods_tag": "",
            # – 可选，trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义
            # "product_id": "111",
            # – 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传”WEB”
            "device_info": "",
            # – 可选，指定支付方式，no_credit–指定不能使用信用卡支付
            "limit_pay": "",
        }

        base_data.update(data)
        print "base_data=", base_data
        return self.pay.order.create(**base_data)

    def get_wechat_token(self):
        s = WECHAT_TOKEN("access_token")
        access_token = s.get_value()
        if access_token:
            print "cache get===access_token"
            return access_token

        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        url = WECHAT_GET_TOKEN_URL % urllib.urlencode(params)
        data = requests.get(url)
        result = data.json()
        access_token = result.get("access_token")
        expire = result.get("expires_in", 7200)
        if not access_token:
            raise Exception
        s.set_value(access_token)
        s.expire(expire)
        return access_token

    def create_menu(self):
        self.client.menu.create(const.MENU)

    def delete_menu(self):
        self.client.menu.delete()

    def check_message(self, xml, data, is_encrypt=True):
        if is_encrypt:
            crypto = WeChatCrypto(self.token, self.aes_key, self.app_id)
            try:
                decrypted_xml = crypto.decrypt_message(
                    xml,
                    data.get("msg_signature"),
                    data.get("timestamp"),
                    data.get("nonce"))
            except (InvalidAppIdException, InvalidSignatureException):
                return None

            msg = parse_message(decrypted_xml)
        else:
            msg = parse_message(xml)

        re_xml = self.parse_msg(msg)

        if is_encrypt:
            return_xml = crypto.encrypt_message(
                    re_xml, data.get("nonce"), data.get("timestamp"))
        else:
            return_xml = re_xml
        return return_xml

    def parse_msg(self, msg):
        print msg.type
        print msg
        if msg.type == "event":
            content = ""
            if msg._data.get("Event", "") == "subscribe":
                content = "1、每日标准上班时间 10:00到19:00；" + \
                    "2、打卡时间10:03之前，之后记为迟到；" + \
                    "3、每月3次以内（含3次）迟到10:30之内，不做处理，" + \
                    "超出3次，从第四次开始累计罚款20 40 80 160 平方递增，" + \
                    "迟到超过30分钟按照事假2小时处理；" + \
                    "4、每人每月带薪病事假1天，不可跨月累计，" + \
                    "超出部分病假发放50%工资（1天以上的需要医院假条）" + \
                    "，事假不发工资；" + \
                    "5、全勤奖，每月无事假病假，及任何迟到显现可获得全勤奖，" + \
                    "奖品每月更换，平均价值300元；" + \
                    "6、加班，每日加班超过22:00（需要管理人员在加班单上签字），" + \
                    "第二天可11:00到岗，周末及节假日加班可累计倒休，抵扣事假，病假。"

            reply = TextReply(message=msg)
            reply.content = content

        elif msg.type == "text":
            reply = TextReply(message=msg)
            reply.content = msg._data.get("Content")

        elif msg.type == "image":
            reply = ImageReply(message=msg)
            reply.media_id = msg._data.get("MediaId")

        elif msg.type == "voice":
            reply = VoiceReply(message=msg)
            reply.media_id = msg._data.get("MediaId")
            pass
        else:
            return None

        re_xml = reply.render()
        return re_xml


wechat = WECHATAPI()
