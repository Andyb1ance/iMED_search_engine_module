import psycopg2

def insert(path):
    conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    sql = "insert into images (path) values ('{0}')".format(path)
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('更新成功')


if __name__ == '__main__':
    insert("/home/andyb1ance/iMED_search_engine_module/myproject/myproject/static/iMed.png")
