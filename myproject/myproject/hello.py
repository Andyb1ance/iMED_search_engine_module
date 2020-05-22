# encoding:utf-8
# !/usr/bin/env python
import string


from flask import Flask, Response,render_template, jsonify, request, make_response, send_from_directory, abort, redirect, url_for
import time
import os
import io
import random
import datetime
import base64
from flask_cors import CORS, cross_origin
from PIL import Image

import CBIRtool
import psycopg2
import uuid
import json

imagepath = '/home/andyb1ance/dataset'
notepath = '/home/andyb1ance/notes'

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF','jpeg','JPEG'])
CORS(app, resources={r'/*': {'origins': '*'}})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/images',methods=['GET'])
def getImage():

# getImage will receive dataset and id of image.
# Using the id to query database ,and get the path of image.
# Resize the image and return it in base64 form.

    dataset = request.args.get('dataset')
    image_id = request.args.get('id')
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    sql = 'select path from {0} where id = {1};'.format(dataset, image_id)
    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    path = rows[0][0]
    print(path)
    im = Image.open(path)
    im.resize((256, 256), Image.ANTIALIAS)
    img_buffer = io.BytesIO()
    im.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    base64_data = base64.b64encode(byte_data)
    s = base64_data.decode()
    conn.close()
    return str(s)

@app.route('/image',methods=['GET'])
def getOneImage():

# getImage will receive dataset and id of image.
# Using the id to query database ,and get the path of image.
# Resize the image and return it in base64 form.

    dataset = request.args.get('dataset')
    image_id = request.args.get('id')
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    sql = 'select path from {0} where id = {1};'.format(dataset, image_id)
    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    path = rows[0][0]
    print(path)
    im = Image.open(path)
    img_buffer = io.BytesIO()
    im.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    base64_data = base64.b64encode(byte_data)
    s = base64_data.decode()
    conn.close()
    return str(s)

@app.route('/up_notes', methods=['POST'], strict_slashes=False)
def upNote():
# upNote receives dataset name , image id and notes
# Store the notes in proper place and store the path in database according to
# dataset name , image id.
    dataset = request.get_json().get('dataset')
    image_id = request.get_json().get('id')
    notes = request.get_json().get('notes')
    uuid_str = uuid.uuid4().hex
    note_file = os.path.join(notepath, uuid_str)
    with open(note_file,'w') as f:
        f.write(notes)
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    table_name = dataset + '_notes'
    note_file = "'" + note_file + "'"
    sql = 'INSERT INTO {0} (image_id, path) VALUES ({1}, {2});'.format(table_name, image_id, note_file)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return notes

@app.route('/down_note', methods = ['GET'],strict_slashes=False)
def downNote():
# downNote receives dataset name and note id
# Select the path of notes according to dataset name  and note id
# Then return the note.
    dataset = request.args.get('dataset')
    note_id = request.args.get('noteId')
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    table_name = dataset + '_notes'
    sql = "select path from {0} where id = {1}".format(table_name, note_id)
    cur.execute(sql)
    rows = cur.fetchall()
    path = rows[0][0]
    with open(path,'r') as f:
        notes = f.read()
    return notes

@app.route('/get_notes', methods = ['GET'],strict_slashes=False)
def getNote():
# getNote receives  dataset name , image id
# return the notes'id belong to the image and dataset
# in form str : 'id1,id2,id3,...,idn'
    image_id = request.args.get('id')
    dataset = request.args.get('dataset')
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    table_name = dataset + '_notes'
    sql = 'select id from {0} where image_id = {1}'.format(table_name, image_id)
    cur.execute(sql)
    rows = cur.fetchall()
    id_list = ''
    for row in rows:
        id_list += row[0] + ','
    id_list = id_list[:-1]
    return id_list

@app.route('/search', methods=['POST'], strict_slashes=False)
def search():
# search receives image and dataset name
# Then search for similar image in the dataset
# and return the id of the similar images
# in form str : 'id1,id2,id3,...,idn'
    dataset = request.files['dataset'] 
    image = request.files['image'] 
    print(dataset)
    print(type(f))
    temp = '1,2,3'
    return temp

# # 上传文件
# @app.route('/up_photo', methods=['POST'], strict_slashes=False)
# def api_upload():
#     # file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
#     # if not os.path.exists(file_dir):
#     #     os.makedirs(file_dir)
#     print("start")
#     f = request.files['photo']
#     print(type(f))
#     a = CBIRtool.frame.Framework("Resnet34","Faiss",'./CBIRtool/encoder/index/sample.index')
#     images = a.search(f,3)
#     conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
#     cur = conn.cursor()
#     img_stream = list()
#     for each in images:
#         sql = 'select img from imgTable limit 1 offset {}'.format(each)
#         cur.execute(sql)
#         rows = cur.fetchall()
#         temp = list()
#         for row in rows:
#             temp.append(str(base64.b64encode(row[0]), encoding='utf-8'))
#         img_stream.append(temp)
#     conn.commit()

#     return render_template('Search.html',u=img_stream)
#     # if f and allowed_file(f.filename):
#     #     fname = secure_filename(f.filename)
#     #     ext = fname.rsplit('.', 1)[1]
#     #     ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#     #     new_filename = ran_str + '.' + ext
#     #     fullPath=os.path.join(file_dir, new_filename)
#     #     f.save(fullPath)

#         # return redirect(url_for('test'))
#     # else:
#     #     return jsonify({"error": 1001, "msg": "上传失败"})

# # @app.route('/test', strict_slashes=False)
# # def test():
# #     #这里应该要把图片做一个处理 变成特征向量
# #     #使用特征向量去数据库索引 标签+图片
# #     #把标签和图片变成数组传过去
# #     images = []
# #     #如果是从url得到图片 则转换成base64
# #     #for i in filename:
# #     #    images.append(return_img_stream(i))
# #     images.append([])
# #     images[0].append(return_img_stream("./upload/12LDT7yX.png"))
# #     images[0].append(return_img_stream("./upload/12LDT7yX.png"))
# #     #images.append("D:\code\iMED_web_front_end\myproject\myproject\upload\AMVJ5Fno.png")
# #     #如果直接是base64图片，则全加到images里发过去
# #     return render_template('Search.html', u=images)


# # def return_img_stream(img_local_path):
# #     with open(img_local_path, 'rb') as f:
# #         image = f.read()
# #     img_stream = str(base64.b64encode(image), encoding='utf-8')
# #     return img_stream

# @app.route('/hello')
# def hello():
#     return render_template('Search.html')

if __name__ == '__main__':
    app.run(threaded = True,debug=False,host='127.0.0.1', port=5000)
