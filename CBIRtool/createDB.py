from transformer import PIL
from extractor import Resnet
from encoder import Faiss
import numpy as np
import psycopg2
import os

def createDB(imageFolder,indexFile):
    images = os.walk(imageFolder)
    e = Resnet.resnet('cpu')
    temp = list()
    fileList = list()
    for path,dir_list,file_list in images:
        fileList = file_list
        for img in file_list:
            #transform picture to 256*256
            t = PIL.transform(os.path.join(imageFolder,img))
            #extract feature and store in list 'temp'
            temp.append(e.extract(t).numpy())
    #construct the index
    Faiss.construct(temp,np.array(temp[0]).shape[0],indexFile) 
    ##加上insert图片的语句..不过faiss是从0自增,可能需要调整.
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432") 
    cur = conn.cursor()
    for img in fileList:
        with open(os.path.join(imageFolder,img),'rb') as f:
            image = f.read()
        sql = "insert into imgTable (img) values ({})".format(psycopg2.Binary(image))
        cur.execute(sql)
    conn.commit()

createDB('./sample','./encoder/index/sample.index')
