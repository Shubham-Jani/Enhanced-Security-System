from django.shortcuts import render
from .models import Profile
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, UserSerializer
from rest_framework import viewsets
import cv2
import face_recognition
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from io import BytesIO
import numpy as np


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


@gzip.gzip_page
def video_feed(request):
    # set up the camera and load the stored face encodings
    cap = cv2.VideoCapture(0)
    # assuming there is at least one profile with face encodings
    profile = Profile.objects.first()
    print(profile.face_encodings)

    # set up the face recognition variables
    known_face_encodings = [
        face_recognition.face_encodings([profile.face_encodings])[0]]
    known_face_names = [profile.user.username]
    print(profile.user)

    # print(known_face_encodings)
    print(known_face_names)

    # define the video streaming function
    def gen():
        while True:
            # read the video frame
            ret, frame = cap.read()
            if not ret:
                break

            # convert the frame from BGR to RGB and resize for faster processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            small_rgb_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

            # compute the face encodings in the frame
            face_locations = face_recognition.face_locations(small_rgb_frame)
            face_encodings = face_recognition.face_encodings(
                small_rgb_frame, face_locations)

            # compare the face encodings against the stored encodings
            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                # find the best match
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                # draw a rectangle and label the face in the frame
                # upscale the face location
                top, right, bottom, left = [pos*4 for pos in face_location]
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            # encode the processed frame as a jpeg image and return it as a response
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = BytesIO(jpeg.tobytes())
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.getvalue() + b'\r\n')

    # return the response as a streaming response
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
