import face_recognition
import os
import numpy as np
from django.conf import settings


def get_encodings_binary(image_name):
    path = f"{settings.BASE_DIR}/{image_name}"
    image = face_recognition.load_image_file(path)
    encodings = face_recognition.face_encodings(image)[0]
    bin_data = encodings.tobytes()
    return bin_data
