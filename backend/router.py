import time
import typing
from sqlalchemy import engine
from backend import clients

def check_alive(connect: engine.base.Connection):
    connect.execute("SELECT 1 + 1")

def reconnect(connect_func: typing.Callable,) -> engine.base.Connection:
    try:
        connect = connect_func()
    except Exception as e:
        print(f"{connect_func.__name__} connect, error {e}")
    return connect

def check_connect_alive(connect: engine.base.Connection, connect_func: typing.Callable,):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            print(f"{connect_func.__name__} connect, error {e}")
            time.sleep(1)
            connect = reconnect(connect_func)
            return check_connect_alive(connect, connect_func)
    else:
        connect = reconnect(connect_func)
        return check_connect_alive(connect, connect_func)

class Router:
    def __init__(self) -> None:
        clients.create_db_if_not_exists()
        clients.create_table_if_not_exist()
        self._mysql_conn = clients.get_mysql_connect()

    def check_mysql_conn_alive(self,):
        self._mysql_conn = check_connect_alive(
            self._mysql_conn, 
            clients.get_mysql_connect
        )

        return self._mysql_conn
    
    @property
    def mysql_conn(self):
        return self.check_mysql_conn_alive()