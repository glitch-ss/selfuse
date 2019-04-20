import mysql.connector

class do_sql():
    def __init__(self):
        self.conn=mysql.connector.connect(host='localhost',user='root',passwd="Atobefuji.900209", port=3306, db='purchase')
        self.cursor=self.conn.cursor()
    
    def send_cmd(self,cmd,err):
        try:
            result = self.cursor.execute(cmd)
            self.conn.commit()
        except Exception, e:
            print e
            print err
    
    def add_item(self, id, name, num, price, status, description):
        cmd = 'insert into items value({0}, "{1}" , {2}, {3}, {4}, "{5}");'.format(id,name, num, price, status, description)
        self.send_cmd(cmd, "fail to add data")
    
    def set_item(self, id, property, val):
        if isinstance(val,str):
            val='"'+val+'"'
        cmd = 'update items set {0} = {1} where id={3};'.format(property, val, id)
        self.send_cmd(cmd, "fail to set data")
        
    def get_item_by_id(self, id):
        cmd = 'select * from items where id={0};'.format(id)
        self.send_cmd(cmd, "fail to get data by id")
        
    def get_items(self):
        cmd = 'select * from items;'
        self.send_cmd(cmd, "fail to get datas")