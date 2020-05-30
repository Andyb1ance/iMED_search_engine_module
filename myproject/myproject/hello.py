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


@app.route('/api/images',methods=['GET'])
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

@app.route('/api/image',methods=['GET'])
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

@app.route('/api/up_notes', methods=['POST'], strict_slashes=False)
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

@app.route('/api/down_note', methods = ['GET'],strict_slashes=False)
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

@app.route('/api/get_notes', methods = ['GET'],strict_slashes=False)
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
        id_list += str(row[0]) + ','
    id_list = id_list[:-1]
    return id_list

@app.route('/api/search', methods=['POST'], strict_slashes=False)
def search():
# search receives image and dataset name
# Then search for similar image in the dataset
# and return the id of the similar images
# in form str : 'id1,id2,id3,...,idn'
    image = request.files['image']
    dataset = request.files['dataset'].read().decode()
    a = CBIRtool.frame.Framework("Resnet34","Faiss",'./CBIRtool/encoder/index/sample.index')
    images = a.search(image,8)
    print(images)
    id_list = ''
    for i in images:
        id_list += str(i) + ','
    id_list = id_list[:-1]
    
    return id_list


if __name__ == '__main__':
    app.run(threaded = True,debug=False,host='0.0.0.0', port=5000)
