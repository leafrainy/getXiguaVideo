#coding:utf8
#下载西瓜视频小助手
#leafrainy
#leafrainy.cc
#2019-06-21

from bs4 import BeautifulSoup as bs
import requests as r
import base64
import execjs
import json


#PC端的西瓜视频连接
videoUrl = "https://www.ixigua.com/i6702721188671521293/"  

header = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

allData = r.get(videoUrl,headers=header)

#获取当前视频及相关视频的json数据
vidData = bs(allData.content,"lxml").find_all("script")[0].get_text().replace("window.__pageState=","")

vidArr = json.loads(vidData)

#核心解密
decryptJs = execjs.compile(""" 

   function getUrl(video_id) {
        var n = function() {
            for (var e = 0, t = new Array(256), n = 0; 256 !== n; ++n)
                e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = n) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1,
                t[n] = e;
            return "undefined" != typeof Int32Array ? new Int32Array(t) : t
        }(), r = "/video/urls/v/1/toutiao/mp4/"+video_id + "?r=" + Math.random().toString(10).substring(2);
        "/" !== r[0] && (r = "/" + r);
        var a = function(e) {
            for (var t, r, o = -1, i = 0, a = e.length; i < a; )
                (t = e.charCodeAt(i++)) < 128 ? o = o >>> 8 ^ n[255 & (o ^ t)] : t < 2048 ? o = (o = o >>> 8 ^ n[255 & (o ^ (192 | t >> 6 & 31))]) >>> 8 ^ n[255 & (o ^ (128 | 63 & t))] : t >= 55296 && t < 57344 ? (t = 64 + (1023 & t),
                r = 1023 & e.charCodeAt(i++),
                o = (o = (o = (o = o >>> 8 ^ n[255 & (o ^ (240 | t >> 8 & 7))]) >>> 8 ^ n[255 & (o ^ (128 | t >> 2 & 63))]) >>> 8 ^ n[255 & (o ^ (128 | r >> 6 & 15 | (3 & t) << 4))]) >>> 8 ^ n[255 & (o ^ (128 | 63 & r))]) : o = (o = (o = o >>> 8 ^ n[255 & (o ^ (224 | t >> 12 & 15))]) >>> 8 ^ n[255 & (o ^ (128 | t >> 6 & 63))]) >>> 8 ^ n[255 & (o ^ (128 | 63 & t))];
            return -1 ^ o
        }(r) >>> 0;
        return ("https://ib.365yg.com"+r + "&s=" + a)                   
    }
	""")

videoJsonUrl = decryptJs.call("getUrl",vidArr['video']['vid'])

videoJsonData = r.get(videoJsonUrl,headers=header)

videoJsonDataArr = json.loads(videoJsonData.content)
#获取最终的视频连接，base64
base64Url = videoJsonDataArr['data']['video_list']['video_3']['main_url']

videoDownloadUrl = str(base64.b64decode(base64Url),'utf-8')

print("视频名称："+vidArr['video']['title'])
print("视频时长(s)："+str(videoJsonDataArr['data']['video_duration']))
print("视频清晰度："+videoJsonDataArr['data']['video_list']['video_3']['definition'])
print("视频格式："+videoJsonDataArr['data']['video_list']['video_3']['vtype'])
print("视频下载地址："+videoDownloadUrl)

