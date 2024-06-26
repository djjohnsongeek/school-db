import pymysql
import traceback

class Database(object):
    def __init__(self, app_config):
        self.conn = None
        self.cursor = None
        self.config = app_config

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.config["DB_HOST"],
            user=self.config["DB_USER"],
            password=self.config["DB_PASSWORD"],
            database=self.config["DB_NAME"],
            charset='utf8mb4',
            port=self.config["DB_PORT"],
            cursorclass=pymysql.cursors.DictCursor
        )

        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, traceback)

        self.cursor.close()
        self.conn.close()

        self.cursor = None
        self.conn = None

    def commit(self):
        self.conn.commit()

    def execute(self, sql: str, args: tuple):
        self.cursor.execute(sql, args)

    def fetchall(self):
        return self.cursor.fetchall()