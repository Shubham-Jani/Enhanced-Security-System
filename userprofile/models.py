from django.db import models
from django.contrib.auth.models import User
from .store_faces import get_encodings_binary
import face_recognition
import numpy as np
import os
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


def get_upload_path(instance, filename):
    """Generate the upload path for an image field."""
    model_name = instance.__class__.__name__.lower()
    folder_name = f"{model_name}_{instance.pk}"
    return os.path.join(folder_name, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    image1 = models.ImageField(upload_to=get_upload_path)
    image2 = models.ImageField(upload_to=get_upload_path)
    image3 = models.ImageField(upload_to=get_upload_path)
    image4 = models.ImageField(upload_to=get_upload_path)
    image5 = models.ImageField(upload_to=get_upload_path)
    face_encodings = models.BinaryField(null=True)
    block_number = models.IntegerField()

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # print(self.image.path)
    #         super(Profile, self).save(*args, **kwargs)
    #         self.face_encodings = get_encodings_binary()
    #     super(Profile, self).save(*args, **kwargs)


# def get_encodings_binary(image_name):
#     path = f"{settings.BASE_DIR}/{image_name}"
#     image = face_recognition.load_image_file(path)
#     encodings = face_recognition.face_encodings(image)[0]
#     bin_data = encodings.tobytes()
#     return bin_data


@receiver(post_save, sender=Profile)
def create_image_folder(sender, instance, **kwargs):
    if kwargs.get('created', False):
        folder_name = str(instance.pk)
        path = os.path.join('media', folder_name)
        if not os.path.exists(path):
            os.mkdir(path)
