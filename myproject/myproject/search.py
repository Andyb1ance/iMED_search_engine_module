from transformer import PIL
from extractor import Resnet
from encoder import Faiss
import psycopg2
import base64

def search(imagePath,indexFile):
    
    e = Resnet.resnet('cpu')
    t = PIL.transform(imagePath)
    distance,index = Faiss.search(e.extract(t),indexFile,2)
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432") 
    cur = conn.cursor()
    for each in index[0]:
        sql = 'select img from imgTable limit 1 offset {}'.format(each)
        cur.execute(sql)
    rows = cur.fetchall()
    img_stream = list()
    for row in rows:
        temp = list()
        temp.append(str(base64.b64encode(row[0]), encoding='utf-8'))
        img_stream.append(temp)
    conn.commit()
    return img_stream
