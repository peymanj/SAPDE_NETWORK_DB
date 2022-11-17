import socket
import traceback
import pyodbc
from source.framework.utilities import log




def log_query(sql, values, e=None):
    msg = sql
    msg = msg + '\n' + 'values: ' + ", ".join([str(i) for i in values]) \
        if values else msg
    if len(msg) > 600:
        msg = msg[:600] + ' ...'

    log(msg, sql='script')
    if e:
        log(e, sql='error')


class Connector:

    # log_level
    LOG_ALL = 1
    LOG_ERROR_ONLY = 2

    def __init__(self, server, port, database, user, password, log_level=LOG_ERROR_ONLY):
        self.server = server
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection_status = False
        self.log_level = log_level
        pass

    def create_connection(self):

        try:
            connection_string = f""" 
                Driver={{ODBC Driver 17 for SQL Server}};
                Server={self.server}; 
                Port={self.port};
                Database={self.database}; 
                UID={self.user};
                PWD={self.password};
                Trusted_Connection=no;
                autocommit=True;
                """

            self.connection = pyodbc.connect(connection_string, autocommit=True)
            # self.connection.execute("PRAGMA foreign_keys = 1")
            self.cursor = self.connection.cursor()
            self.connection_status = True

        except Exception as e:
            traceback.print_exc()
            print('error connection to db' + str(e))
            self.connection_status = False

        return self.connection_status

    def close_db(self):
        if self.connection_status:
            self.cursor.close()
            self.connection.close()
            self.connection_status = False
            return True
        else:
            return False

    def run_sql(self, sql_raw, values=None, header=True, ddl=False):
        try:
            queryset = list()
            query_run_status = False

            sql = sql_raw.replace('\n', ' ')
            if not self.connection_status:
                self.create_connection()
            if values:
                self.cursor.execute(sql, values)
            else:
                self.cursor.execute(sql)
            if ddl:
                while self.cursor.nextset():
                    pass
            try:
                data = self.cursor.fetchall()
            except:
                data = None
            if header and data:
                queryset = list()
                desc = self.cursor.description
                column_names = [col[0] for col in desc]
                for row in data:
                    for i in range(len(row)):
                        if row[i] == 'False':
                            row[i] = False
                        elif row[i] == 'True':
                            row[i] = True
                    queryset.append(dict(zip(column_names, row)))

            elif not header and data:
                queryset = data

            query_run_status = True
            # if len(queryset) == 1:
            #     queryset = queryset[0]
            if self.log_level == self.LOG_ALL:
                log_query(sql_raw, values)
            return queryset, query_run_status

        except Exception as e:

            log_query(sql_raw, values, e)
            query_run_status = False
            self.close_db()
            return e, query_run_status


