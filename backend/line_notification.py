import requests
import os
import base64
import datetime
from backend.db import request_updated_post, update_post_status


def divide_chunks(l: list, n: int):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def send(message: str):
    line_token = os.getenv('LINE_TOKEN')
    headers = {"Authorization": "Bearer " + line_token}
    data = {'message': message}
    try:
        requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, data=data)
    except TimeoutError:
        print("Line notification timeout!")
    except Exception as e:
        print(e)


def send_message():
    request_data = request_updated_post()
    for data in request_data:
        url = data["url"]
        encoded_pushes = data["pushes"]
        decoded_pushes = base64.b64decode(encoded_pushes).decode("utf8")
        push_list = decoded_pushes.split("\n")
        message = f"https://www.ptt.cc/bbs/Stock{url}\n"
        for index, pushes in enumerate(divide_chunks(push_list, 10)):
            send(message + "\n".join(pushes))
        update_post_status(url)
    send(f"PTT Stock at {datetime.datetime.today()}.")
