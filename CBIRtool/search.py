from transformer import PIL
from extractor import Resnet
from encoder import Faiss
import psycopg2

# def search(imagePath,indexFile):
    
#     e = Resnet.resnet('cpu')
#     t = PIL.transform(imagePath)
#     Faiss.search(e.extract(t),indexFile,2)


conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432") 
cur = conn.cursor()

sql = 'select img from imgTable limit 1 offset 1'
cur.execute(sql)
rows = cur.fetchall()

print(type(rows))
for row in rows:
    with open('test.jpeg','wb') as file:
    	file.write(row[0])
    


conn.commit()
