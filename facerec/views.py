import cv2
import face_recognition
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.conf import settings
from userprofile.models import Profile
import numpy as np
from django.shortcuts import render
from django.contrib.auth.models import User
# This is a generator function that will continuously read frames from the webcam


def webcam_stream():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n'

# This view will stream the video from the webcam to the user's browser


@gzip.gzip_page
def webcam_feed(request):
    return StreamingHttpResponse(webcam_stream(), content_type='multipart/x-mixed-replace; boundary=frame')

# This view will process the frames from the webcam and display the name of the person in the frame, if any


def webcam_recognition(request):
    # Get the encodings of all the known faces from the database
    known_encodings = Profile.objects.all().values_list('face_encodings', flat=True)
    print(known_encodings)

    # Convert the string encodings to numpy arrays
    known_encodings = [face_recognition.face_encodings(np.fromstring(
        encoding, dtype=np.float64))[0] for encoding in known_encodings]

    # Process the frames from the webcam
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces in the frame and compute their encodings
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Match the detected face encodings with the known face encodings
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_encodings, face_encoding)
            if True in matches:
                # Display the name of the person in the frame
                name = Profile.objects.get(
                    face_encoding=np.array2string(face_encoding)).name
                cv2.putText(
                    frame, name, (face_locations[3], face_locations[0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convert the frame to a string and send it to the user's browser
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def index(request):
#     known_encodings = Profile.objects.all().values_list('face_encodings', flat=True)
#     # Convert the string encodings to numpy arrays
#     known_encodings = [np.frombuffer(
#         encoding, dtype=np.float64) for encoding in known_encodings]
#     # print(known_encodings)
#     try:
#         return render(request, 'test.html')
#     except cv2.error as e:
#         print(e)


def index(request):
    # Load known face encodings from database
    known_face_encodings = []
    known_face_names = []
    users = User.objects.all()
    # faces = Face.objects.all()
    for user in users:
        if user.is_staff:
            continue
        face_encodings = np.frombuffer(user.profile.face_encodings)
        known_face_encodings.append(face_encodings)

        known_face_names.append(user.username)

    # Initialize webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)

            # If there's a match, display the name of the user
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release webcam and close window
    video_capture.release()
    cv2.destroyAllWindows()

    return render(request, 'test.html')
