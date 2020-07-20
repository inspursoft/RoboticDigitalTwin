#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import *
import os
import json
from time import sleep
import requests
import gevent
from gevent import monkey
monkey.patch_all()


HTML = """
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>file uploader</title><style type="text/css">body{font-size:14px;align-text:center}input{vertical-align:middle;margin:0;padding:0}.file-box{position:relative;width:340px;margin:0 auto}.txt{height:22px;border:1px solid #cdcdcd;width:180px}.btn{height:24px;width:70px}.file{position:absolute;top:0;right:80px;height:24px;filter:alpha(opacity:0);opacity:0;width:260px}</style></head><body><div class="file-box"><form action="/upload" method="post" enctype="multipart/form-data" id="uploader"><input type='text' name='textfield' id='textfield' class='txt' /><input type='button' class='btn' value='浏览...' /><input type="file" capture="environment" name="fileField" class="file" id="fileField" size="28" /><input type="submit" name="submit-btn" id="upload" class="btn" value="上传" onclick="onUploading()"/></form></div><div style="text-align: center"><img src="" alt="previewer" id="previewer" style="margin-top: 15px;max-width: 640px;max-height: 480px;border: 3px dashed black;" hidden="true"></div><script type="text/javascript">function onUploading(){var load = document.getElementById('upload');load.disabled=true;load.value = '上传中';setInterval(()=>{var value = load.value;load.value = value.length>8?'上传中':value+'.'},500);document.getElementById('uploader').submit()}function getFileURL(file){let getUrl = null;if(window.createObjectURL!== undefined){getUrl = window.createObjectURL(file)}else if(window.URL!== undefined){getUrl = window.URL.createObjectURL(file)}else if(window.webkitURL!== undefined){getUrl = window.webkitURL.createObjectURL(file)}return getUrl}let fileElement = document.getElementById("fileField");let imgElement = document.getElementById("previewer");fileElement.onchange = function(){document.getElementById('textfield').value=this.value;imgElement.hidden = false;let url = getFileURL(fileElement.files[0]);imgElement.setAttribute("src",url)};</script></body></html>
"""


base_path = os.path.dirname(os.path.realpath(__file__))  # 获取脚本路径
pos = {"left": "red"}

upload_path = os.path.join(base_path, 'upload')   # 上传文件目录
if not os.path.exists(upload_path):
    os.makedirs(upload_path)


def getRedPos(path):
    try:
        file = {'file': open(path, 'rb')}
        new_url = 'http://10.111.25.27:13856'
        res = requests.post(url=new_url, files=file)
        return res.text
    except Exception as e:
        raise e


@route('/', method='GET')
@route('/upload', method='GET')
@route('/index.html', method='GET')
@route('/upload.html', method='GET')
def index():
    """显示上传页"""
    return HTML


@route('/upload', method='POST')
def do_upload():
    """处理上传文件"""
    global pos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

    try:
        filedata = request.files.get('fileField')
        print(filedata)

        if filedata.file:
            file_name = os.path.join(upload_path, filedata.filename)
            try:
                filedata.save(file_name)  # 上传文件写入
                yield template("上传文件成功, 正在解析: {{file_name}}<br>", file_name=filedata.filename)
                res = getRedPos(file_name)
                rate = json.loads(res)
                print("red_left:", float(rate["red_left"]),
                    "red_right:", float(rate["red_right"]))
                if float(rate["red_left"]) < float(rate["red_right"]):
                    pos["left"] = "blue"
                else:
                    pos["left"] = "red"
                print("rate:", rate, "    pos:", pos)

                posFile = os.path.join(upload_path, 'pos.txt')
                with open(posFile, 'w') as file_object:
                    file_object.write(json.dumps(pos))
                yield template('解析结果: {{res}}<br><a href="/upload">返回</a>', res=res)
            except IOError as e1:
                yield template('保存文件失败: {{e1}}<br><a href="/upload">返回</a>', e1=e1)
            except Exception as e2:
                yield template('解析失败: {{e2}}<br><a href="/upload">返回</a>', e2=e2)
        else:
            yield template("上传文件成功, 正在解析: {{file_name}}<br>", file_name=file_name)
    except Exception as e:
        print(e)
        yield template('未知错误: {{e}}<br><a href="/upload">返回</a>', e=e)

# @route('/favicon.ico', method='GET')
# def server_static():
#     """处理网站图标文件, 找个图标文件放在脚本目录里"""
#     return static_file('favicon.ico', root=base_path)


@route('/getPos', method='GET')
def getPos():
    global pos
    return json.dumps(pos)


@error(404)
def error404(error):
    """处理错误信息"""
    return '404 发生页面错误, 未找到内容'


run(host='0.0.0.0', port=8080, server='gevent')
