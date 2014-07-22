#!/usr/bin/env python
# -*- coding: utf-8  -*-

"""
Created by qingyun.meng on 2014-7-21.
Description: Rong Cloud Auth Service Template.
"""
import urllib
import urllib2
from urllib2 import HTTPError

RONGCLOUD_CONF = {
    "app_key": "your_appkey",
    "app_secret": "your_appsecret",
    "api_host": "http://auth.cn.rong.io"
}


class FORMAT:
    JSON = 'json'
    XML = 'xml'


class BaseService(object):

    def get_response(self, url, data=None, headers=None, method='POST'):
        """
        get http response
        :param url: service url
        :param data: post/get form data
        :param headers: request headers
        :param method: request method
        :return: tuple: (code, msg, response_body,)  
        """
        if not headers:
            headers = {}

        url = urllib.basejoin(RONGCLOUD_CONF['api_host'], url)

        headers.update({
            "Content-Type": "Application/x-www-form-urlencoded",
            'appKey': RONGCLOUD_CONF['app_key'],
            'appSecret': RONGCLOUD_CONF['app_secret'],
        })
        params = urllib.urlencode(data)

        if method.upper() == 'GET':
            url = '%s?%s' % (url, params)
            req = urllib2.Request(url, headers=headers)
        else:
            req = urllib2.Request(url, params, headers=headers)
        try:
            res_data = urllib2.urlopen(req)
            response = res_data.read()
            return_back = res_data.code, res_data.msg, response
        except HTTPError, ex:
            return_back = ex.code, ex.msg, None
        else:
            res_data.close()
        return return_back


class Auth(BaseService):
    service_url = '/reg.%(format)s'
    method = 'POST'
  
    def request(self, user_id, name='', portrait_uri='', device_id='', format=FORMAT.JSON):
        """
        userId	    String	用户 Id，最大长度 32 字节，是用户在 App 中的唯一标识码，必须保证在同一个 App                              内不重复，重复的用户 Id 将被当作是同一用户。
        name	      String	用户名称，最大长度 128 字节。
        portraitUri	String	用户头像 URI，最大长度 1024 字节。
        deviceId	  String	设备 Id，设备的唯一标识，用来在推送中识别设备。
        """

        params = {
            'userId': user_id,
            'name': name,
            'portraitUri': portrait_uri,
            'deviceId': device_id
        }
        url = self.service_url % {'format': format}
        return self.get_response(url, params, method=self.method)


if __name__ == '__main__':
    result = Auth().request(1, name='test', portrait_uri='your_uri',device_id='IOS7', format=FORMAT.JSON)
    print result
