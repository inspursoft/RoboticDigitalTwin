from bottle import route, run
import os

base_path = os.path.dirname(os.path.realpath(__file__))  # 获取脚本路径

upload_path = os.path.join(base_path, 'upload')   # 上传文件目录
if not os.path.exists(upload_path):
    os.makedirs(upload_path)

@route('/', method='GET')
@route('/getPos', method='GET')
def getPos():
    posFile = os.path.join(upload_path, 'pos.txt')
    with open(posFile, 'r') as f:
        res = f.read()
        print(res)
        return res
    return "Not Ready"


run(host='0.0.0.0', port=8080)