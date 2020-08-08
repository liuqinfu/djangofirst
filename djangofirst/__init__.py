import pymysql
#解决使用mysql启动时报错：mysqlclient 1.4.0 or newer is required
pymysql.version_info = (1, 4, 13, "final", 0)
# 替换自带的sqlite
pymysql.install_as_MySQLdb()