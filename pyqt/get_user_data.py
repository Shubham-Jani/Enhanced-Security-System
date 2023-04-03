import requests
import numpy as np


def get_users():
    url = "http://127.0.0.1:8000/users/users/"
    response = requests.get(url)
    if response.status_code == 200:
        datas = response.json()
        for data in datas:
            if data['is_staff'] == True:
                continue
            data['profile']['face_encodings'] = np.fromstring(
                data['profile']['face_encodings'])
            print(type(data['profile']['face_encodings']))
        return datas


get_users()
