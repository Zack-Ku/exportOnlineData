import configparser
import pymysql
import json

class generator:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read('db.ini')
        host = cf.get('database-conn', 'host')
        port = cf.get('database-conn', 'port')
        username = cf.get('database-conn', 'username')
        password = cf.get('database-conn', 'password')
        db = cf.get('database-conn', 'db')

        self.limit = int(cf.get('export-conf', 'limit'))
        self.tables = json.loads(cf.get('export-conf', 'tables'))
        print(u"打开db链接")
        self.conn = pymysql.connect(host, username, password, db, int(port))
        self.cursor = self.conn.cursor()

    def close(self):
        print(u"关闭链接")
        self.cursor.close()
        self.conn.close()

    def parse_data(self, row):
        parse_str = ""
        # print(row)
        for index in range(len(row)):
            column = row[index]
            if index != 0:
                parse_str = parse_str + ','
            if isinstance(column, (int, float)):
                parse_str = parse_str + str(column)
            elif isinstance(column, str):
                parse_str = parse_str + "'%s'" % column
            elif column is None:
                parse_str = parse_str + "NULL"
            else:
                parse_str = parse_str + str(column)

        return parse_str

    def write_file(self, file, sql, rows):

        for row in rows:
            parse_str = self.parse_data(row)
            # print(sql % parseStr)
            file.write(sql % parse_str)

    def export_data(self):
        for table in self.tables:
            print("开始导出%s" % table)
            offset = 0
            count = 0
            path = "./out/" + table + ".sql"
            file = open(path, "w+")
            while True:
                self.cursor.execute("select * from %s limit %d,%d" % (table, offset, self.limit))
                rows = self.cursor.fetchall()
                if len(rows) < 1:
                    break
                sql = "insert into " + table + "values (%s);\n"
                self.write_file(file, sql, rows)
                count += len(rows)
                offset += self.limit
                print("导出%s，%d条" % (table, len(rows)))
            print("导出%s完毕，共%d条" % (table, count))
            file.close()
