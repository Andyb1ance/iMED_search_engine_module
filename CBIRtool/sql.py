import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                             database='test',
                                             user='root',
                                             password='451253745')

with open('./sample/13_left.jpeg',mode ='rb') as f:
    img = f.read()
print(type(img))
cursor = connection.cursor()
query = 'insert into mytable (fID,photo) values (%s,%s)'
cursor.execute(query,(0,img))
connection.commit()
cursor.close()
connection.close()