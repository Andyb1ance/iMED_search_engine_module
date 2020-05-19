import os
import psycopg2

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

if __name__ == '__main__':
        directory = '/home/andyb1ance/dataset/1_normal'
        insert(directory, 'normal')
        directory = '/home/andyb1ance/dataset/2_glaucoma'
        insert(directory, 'glaucoma')
        directory = '/home/andyb1ance/dataset/2_cataract'
        insert(directory, 'cataract')
        directory = '/home/andyb1ance/dataset/3_retina_disease'
        insert(directory, 'retina')