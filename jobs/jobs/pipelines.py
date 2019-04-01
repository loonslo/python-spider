# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi


class JobsPipeline(object):
    def process_item(self, item, spider):
        return item


class LaGouPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1', 'root', '123456', 'jobs', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
               insert into jobs (url, url_object_id, title, salary, job_city, work_years, degree_need, job_type, publish_time,tags, job_advantage, job_detail, job_addr, company_url, company_name, crawl_time)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               """

        params = (item['url'], item['url_object_id'], item['title'], item['salary'], item['job_city'],
                  item['work_years'], item['degree_need'], item['job_type'], item['publish_time'], item['tags'],
                  item['job_advantage'], item['job_detail'], item['job_addr'],
                  item['company_url'], item['company_name'], item['crawl_time'])
        self.cursor.execute(insert_sql, params)
        self.conn.commit()


class LaGouTwistedPipeline(object):

    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db_parms = dict(
            host=settings["MYSQL_HOST"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            db=settings["MYSQL_DBNAME"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool("pymysql", **db_parms)

        return cls(db_pool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.db_pool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
                      insert into jobs (url, url_object_id, title, salary, job_city, work_years, degree_need, job_type, publish_time,tags, job_advantage, job_detail, job_addr, company_url, company_name, crawl_time)
                      values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                      """
        params = (item['url'], item['url_object_id'], item['title'], item['salary'], item['job_city'],
                  item['work_years'], item['degree_need'], item['job_type'], item['publish_time'], item['tags'],
                  item['job_advantage'], item['job_detail'], item['job_addr'],
                  item['company_url'], item['company_name'], item['crawl_time'])

        cursor.execute(insert_sql, params)
