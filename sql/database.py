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

    # def check(self): # 改成一个table的初始化函数，因为表的生成是最后的一步，所以存在表，就清空，不存在就创建表
    def table_init(self):
        sql = 'show tables'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result = str(result)
        if result.find(self.table) >= 0:
            print('Table %s already exists.' %self.table)
            return True
        else:
            return False

    def create_table(self):
        # if self.check():
        #     return

        # 每次开始时，先连接数据库 我也不知道是在init里面self比较好，还是每次函数开始都连接数据库比较好，你看着办
        # db, cursor = self.connect()


        self.table_init()

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
        """     ### 可以用字段name可以用text吗？（疑问句）
        self.cursor.execute(sql)
        self.close() # 创建完就关闭

def main():
    knife = Database('localhost', 'root', 'root', 'test', 'knife')
    knife.connect()
    knife.create_table()

if __name__ == '__main__':
    main()
