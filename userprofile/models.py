from django.db import models
from django.contrib.auth.models import User
from .store_faces import get_encodings_binary
import face_recognition
import numpy as np
import os
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to='user_images/')
    face_encodings = models.BinaryField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # print(self.image.path)
            super(Profile, self).save(*args, **kwargs)
            self.face_encodings = get_encodings_binary(self.image.name)
        super(Profile, self).save(*args, **kwargs)


# def get_encodings_binary(image_name):
#     path = f"{settings.BASE_DIR}/{image_name}"
#     image = face_recognition.load_image_file(path)
#     encodings = face_recognition.face_encodings(image)[0]
#     bin_data = encodings.tobytes()
#     return bin_data
