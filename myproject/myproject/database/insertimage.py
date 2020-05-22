import os
import psycopg2
import uuid

def insert(rootdir,table):
        conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        list = os.listdir(rootdir)
        for i in range(0, len(list)):
                com_path = os.path.join(rootdir, list[i])
                if os.path.isfile(com_path):
                        com_path = "'" + com_path + "'"
                        sql = 'INSERT INTO {0} (path) VALUES ({1});'.format(table, com_path)
                        cur.execute(sql)
                        conn.commit()
        conn.close()

notepath = '/home/andyb1ance/notes'

if __name__ == '__main__':
        dataset = 'cataract'
        image_id = 1
        conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        table_name = dataset + '_notes'
        sql = 'select id from {0} where image_id = {1}'.format(table_name, image_id)
        print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        id_list = ''
        for i in rows:
            id_list += str(i[0]) + ','
        id_list = id_list[:-1]
        print(id_list)
        conn.close()
