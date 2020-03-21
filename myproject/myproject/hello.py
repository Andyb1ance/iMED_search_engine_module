# encoding:utf-8
# !/usr/bin/env python
import string

from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort, redirect, url_for
import time
import os
import random
import datetime
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        new_filename = ran_str + '.' + ext
        fullPath=os.path.join(file_dir, new_filename)
        f.save(fullPath)

        return redirect(url_for('test'))
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})

@app.route('/test', strict_slashes=False)
def test():
    #这里应该要把图片做一个处理 变成特征向量
    #使用特征向量去数据库索引 标签+图片
    #把标签和图片变成数组传过去
    images = []
    #如果是从url得到图片 则转换成base64
    #for i in filename:
    #    images.append(return_img_stream(i))
    images.append([])
    images[0].append(return_img_stream("D://code//iMED_web_front_end//myproject//myproject//upload//12LDT7yX.png"))
    images[0].append(return_img_stream("D://code//iMED_web_front_end//myproject//myproject//upload//12LDT7yX.png"))
    #images.append("D:\code\iMED_web_front_end\myproject\myproject\upload\AMVJ5Fno.png")
    #如果直接是base64图片，则全加到images里发过去
    return render_template('Search.html', u=images)


def return_img_stream(img_local_path):
    with open(img_local_path, 'rb') as f:
        image = f.read()
    img_stream = str(base64.b64encode(image), encoding='utf-8')
    return img_stream

@app.route('/hello')
def hello():
    return render_template('Search.html')

if __name__ == '__main__':
    app.run(debug=True)