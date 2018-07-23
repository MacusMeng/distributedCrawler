# -*- coding:utf-8 -*-
# Hello world - 西蒙.科泽斯 这是“向编程之神所称颂的传统咒语，愿他帮助并保佑你更好的学习这门语言
import pymysql
import redis
from scrapy.utils.project import get_project_settings


class RedisHelper():
    def __init__(self):
        self.settings = get_project_settings()
        self.redis_host = self.settings.get('REDIS_HOST')
        self.redis_port = self.settings.get('REDIS_PORT')
        self.rediscli = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=0)


class MysqlHelper():
    """
        mysql 工具类
        2018年2月26日14:32:34
    """

    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings.get('MYSQL_HOST')
        self.port = self.settings.get('MYSQL_PORT')
        self.db = self.settings.get('MYSQL_DBNAME')
        self.user = self.settings.get('MYSQL_USER')
        self.passwd = self.settings.get('MYSQL_PASSWD')
        self.charset = self.settings.get('MYSQL_CHARSET')

    def connect(self):
        # 连接数据库
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e.message)
        return result

    def get_all(self, sql, params=()):
        list = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e.message)
        return list

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e.message)
        return count
