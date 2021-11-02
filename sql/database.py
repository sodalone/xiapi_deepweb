import pymysql

class Database:

    def __init__(self, table_name, host='127.0.0.1', user='root', password='123456', database='xiapi'):
        self.table_name = table_name
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.db, self.cursor = self.connect()

    def connect(self):
        db = pymysql.connect(
             host=self.host,
             user=self.user,
             password=self.password,
             database=self.database
        )
        cursor = db.cursor()
        return db, cursor

    def close(self):
        self.cursor.close()
        self.db.close()

    #table的初始化函数,存在表，就清空
    def table_init(self):
        sql = 'show tables'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result = str(result)
        if result.find(self.table_name) >= 0:
            clear_table = 'truncate table %s' %self.table_name
            self.cursor.execute(clear_table) #清空表，但表的结构还在
            print('Table %s already exists. Delete the old and create a new table.' %self.table_name)
            return True
        else:
            return False

    def create_table(self):
        exist = self.table_init()
        if not exist:
            sql = f"""
                create table {self.table_name}(itemid_shopid_catid varchar(50) not null primary key,
                similiar_flag int,
                name varchar(200), 
                price varchar(50),
                price_before_discount varchar(50),
                discount float,
                rating_star float,
                historical_sold int,
                comment_count int)ENGINE=innodb DEFAULT CHARSET=utf8;
            """     # 可以用字段name可以用text吗？（疑问句）
            self.cursor.execute(sql)

    def query(self):
        query_data = 'select * from %s' %self.table_name
        self.cursor.execute(query_data)
        result = self.cursor.fetchall()
        result = str(result[0])
        print(result)

def main():
    knife = Database('knife', 'localhost', 'root', 'root', 'test')
    knife.connect()
    knife.create_table()
    knife.query()
    knife.close() #所有操作进行完毕后必须执行close

if __name__ == '__main__':
    main()
