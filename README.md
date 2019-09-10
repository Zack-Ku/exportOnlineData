# 导出线上数据
### export online data without permission
目前只支持mysql数据导出

feature:
1. 用于导出线上没有导出权限，但有查询权限的情况。   
2. 直接导出数据的insert 语句。
3. 分页导出，默认5000条一页。
4. 支持配置多表，配置tables。

使用方法：
1. 修改db.ini 的配置。修改db链接，修改导出表 tables
2. 执行 python run.py
3. 在 out 目录查看导出的insert sql

运行环境，python3.7   
可能需要安装的库 pymysql
