from backend.router import Router
from typing import ByteString
import base64
from sqlalchemy import exc

router = Router()


def check_post_status(post_url: str, encoded_message: ByteString) -> bool:
    db_conn = router.mysql_conn
    trans = db_conn.begin()
    sql_cmd = f"""
            SELECT pushes
            FROM post
            WHERE url = '{post_url}'
        """
    request_data = db_conn.execute(sql_cmd).first()
    trans.commit()
    if request_data["pushes"] == encoded_message:
        return False
    return True


def save_post_to_db(result_post_obj: dict):
    if result_post_obj.get("valid", False):

        url = result_post_obj["url"]
        slash_index = url.rfind("/")
        url = url[slash_index:]

        author = result_post_obj["author"]
        nick_name_index = author.find('(')
        if nick_name_index != -1:
            author = author[:nick_name_index]
        encoded_author = base64.b64encode(
            author.encode('utf-8')).decode("utf-8")

        push_message = ""
        for push in result_post_obj.get("push", []):
            push_message += push + "\n"
        encoded_pushes = base64.b64encode(
            push_message.encode('utf-8')).decode("utf-8")

        db_conn = router.mysql_conn
        trans = db_conn.begin()
        try:
            sql_cmd = f"""
                    INSERT INTO post (url, author, pushes, status)
                    VALUES ('{url}', '{encoded_author}', '{encoded_pushes}', 'Y')
                """
            db_conn.execute(sql_cmd)
        except exc.SQLAlchemyError as e:
            if check_post_status(url, encoded_pushes):
                sql_cmd = f"""
                        UPDATE post SET pushes = '{encoded_pushes}', status = 'Y'
                        WHERE url = '{url}'
                    """
                db_conn.execute(sql_cmd)
                print(f"{url} updated.")
            else:
                print(f"{url} is the latest.")

        trans.commit()


def request_updated_post():
    db_conn = router.mysql_conn
    trans = db_conn.begin()
    request_sql_cmd = f"""
            SELECT *
            FROM post
            WHERE status = 'Y'
        """
    request_data = db_conn.execute(request_sql_cmd)
    trans.commit()
    return request_data


def update_post_status(url: str):
    db_conn = router.mysql_conn
    trans = db_conn.begin()
    update_sql_cmd = f"""
            UPDATE post SET status = 'N'
            WHERE url = '{url}'
        """
    db_conn.execute(update_sql_cmd)
    trans.commit()
