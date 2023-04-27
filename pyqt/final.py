import sys
sys.path.append('/media/data_s/Programs/vvp_hackathon/webapp')
from django_setup import *
import PySimpleGUI as sg
import cv2
import datetime
from userprofile.models import Profile
from django.contrib.auth.models import User
import face_recognition
import numpy as np




# Define the capture object to get frames from the webcam
cap = cv2.VideoCapture(1)
users = User.objects.all()
known_face_encodings = []
known_face_ids = []
for user in users:
    if user.is_staff:
        continue
    face_encodings = np.frombuffer(user.profile.face_encodings)
    known_face_encodings.append(face_encodings)
    known_face_ids.append(user.pk)
    print(known_face_ids)


# Create a layout with a frame and an image element inside the frame
layout = [
    [sg.Frame('Camera Feed', [[sg.Image(key='-IMAGE-')]]),
     sg.Frame('', [
         [sg.Frame('Date and Time', [[sg.Text("Date:"), sg.Text(key="-DATE-")],
                                     [sg.Text("Time"), sg.Text(key="-TIME-")]]),],
         [sg.Frame('Details: ', [
                                [sg.Image(key='-FACE-')],
                                [sg.Text("Name:"), sg.Text(key='-NAME-')],
             [sg.Text("Block Number:"), sg.Text(key='-BLOCK-')]])]
     ])
     ],
    [sg.Button('Exit'), sg.Button('STOP/Start', key="-REC-")]
]

# sg.theme('LightBrown')
# Create the window with a size of 640x480 and display it
window = sg.Window('Webcam Feed in PySimpleGUI', layout)
is_face_recognized = False
while True:
    event, values = window.read(timeout=20)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # Get a new frame from the webcam
    ret, frame = cap.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    if ret:
        # convert the frame to RGB image
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if (is_face_recognized == False):
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                is_face_recognized = True
                face_encodings = face_recognition.face_encodings(
                    frame, face_locations)
                cropped_face_frame = frame[top-40:bottom+30, left-20:right+20]
                cropped_face = cv2.imencode(
                    '.png', cropped_face_frame)[1].tobytes()
                window['-FACE-'].update(cropped_face)
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.5)
                print(matches)
                if True in matches:
                    first_match_index = matches.index(True)
                    user = User.objects.get(
                        id=known_face_ids[first_match_index])
                    name = user.username
                    # name = self.knownusers[first_match_index+1]["username"]
                    print(first_match_index)
                    id = known_face_ids[first_match_index]

                    cv2.putText(frame, name, (left + 6, bottom - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
                    block = user.profile.block_number
                    window['-NAME-'].update(name)
                    window['-BLOCK-'].update(block)
    # Convert the frame to a format that PySimpleGUI can display
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()

    # Update the image element in the PySimpleGUI window with the new frame
    window['-IMAGE-'].update(imgbytes)
    window['-DATE-'].update(datetime.date.today())

    window['-TIME-'].update(datetime.datetime.now().strftime('%H:%M:%S'))

# Release the webcam and close the window
cap.release()
window.close()
