from django.db import models
from django.contrib.auth.models import User
from .store_faces import get_encodings_binary
import face_recognition
import numpy as np
import os
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import face_recognition
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    image1 = models.ImageField(upload_to="images/")
    image2 = models.ImageField(upload_to="images/")
    image3 = models.ImageField(upload_to="images/")
    image4 = models.ImageField(upload_to="images/")
    image5 = models.ImageField(upload_to="images/")
    face_encodings = models.BinaryField(null=True)
    block_number = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
            return
        # call the parent class's save method
        super().save(*args, **kwargs)

        # loop through the image fields and compute the face encodings
        image_fields = [self.image1, self.image2,
                        self.image3, self.image4, self.image5]
        face_encodings = []
        print(len(image_fields))
        for image in image_fields:
            print(type(image))
            print(image.path)
            # check if image exists
        #     if not image_field:
        #         continue

        #     # load the image data
            image_data = BytesIO(image.read())

            # compute the face encodings for the image
            image = face_recognition.load_image_file(image.path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                face_encodings.extend(encoding)
             # store the face encodings as a binary blob in the profile
            if face_encodings:
                print(face_encodings)
                encoding_bytes = face_encodings[0].tobytes()
                self.face_encodings = encoding_bytes
                self.save(update_fields=['face_encodings'])


class Log(models.Model):
    resident = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="logs", null=True)
    picture = models.ImageField(upload_to="logs/image/")
    time = models.DateTimeField(auto_now_add=True)
