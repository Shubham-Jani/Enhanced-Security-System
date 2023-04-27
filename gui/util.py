import sys

sys.path.append('/media/data_s/Programs/vvp_hackathon/webapp')
from django_setup import *


from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
import cv2
import face_recognition
import numpy as np
from userprofile.models import Profile, Log
from django.contrib.auth.models import User
import datetime
import PySimpleGUI as sg
import time



def get_stored_encodings():
    users = User.objects.all()
    known_face_encodings = []
    known_face_ids = []
    for user in users:
        if user.is_staff:
            continue
        face_encodings = np.frombuffer(user.profile.face_encodings)
        known_face_encodings.append(face_encodings)
        known_face_ids.append(user.pk)
    return known_face_encodings, known_face_ids


def recognize_faces(frame, face_locations, known_face_encodings, known_face_ids):
    names = []
    blocks = []
    ids = []
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding, tolerance=0.5)
        if True in matches:
            first_match_index = matches.index(True)
            user = User.objects.get(id=known_face_ids[first_match_index])
            name = user.username
            ids.append(known_face_ids[first_match_index])
            names.append(name)
            block = user.profile.block_number
            blocks.append(block)
        else:
            names.append(None)
            blocks.append(None)
    return names, blocks, ids


def update_gui(window, frame, face_locations, names, blocks):
    cropped_face = None
    is_resident = False
    for (top, right, bottom, left), name, block in zip(face_locations, names, blocks):
        if name is not None:
            is_resident = True
            try:
                cropped_face_frame = frame[top-70:bottom+20, left-20:right+20]
                cropped_face = cv2.imencode(
                    '.png', cropped_face_frame)[1].tobytes()
                window['-FACE-'].update(cropped_face)
            except:
                pass
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
            window['-NAME-'].update(name)
            window['-BLOCK-'].update(block)
        else:
            try:
                cropped_face_frame = frame[top-70:bottom+20, left-20:right+20]
                cropped_face = cv2.imencode(
                    '.png', cropped_face_frame)[1].tobytes()
                window['-FACE-'].update(cropped_face)
            except:
                pass
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    webcam_image = cv2.imencode('.png', frame)[1].tobytes()
    window['-IMAGE-'].update(webcam_image)
    return is_resident, cropped_face


def update_date_time(window):
    window['-DATE-'].update(datetime.date.today())
    window['-TIME-'].update(datetime.datetime.now().strftime('%H:%M:%S'))


def open_gate(window, events, ids, cropped_face, cap):
    # Create an image object from the bytes
    image = Image.open(BytesIO(cropped_face))

    # Save the image to a memory buffer
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)

    # Create an InMemoryUploadedFile from the memory buffer
    image_file = InMemoryUploadedFile(
        buffer, None, 'image.jpg', 'image/jpeg', buffer.getbuffer().nbytes, None
    )

    user = User.objects.get(id=ids[0])
    log = Log.objects.create(resident=user, picture=image_file)
    log.save()
    print(ids)
    print("The gate will open now and log will be saved")
    sg.popup("Gate is Opening", auto_close=True, auto_close_duration=5)
    start_time = time.time()
    while (time.time() - start_time) < 5:
        ret, frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Define the popup layout
    popup_layout = [
        [sg.Text("Please enter some text:")],
        [sg.Input(key="-TEXT-")],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    # Create the popup window
    popup_window = sg.Window("Popup", layout=popup_layout, modal=True)

    # Loop until the popup window is closed
    while True:
        popup_event, popup_values = popup_window.read()

        # If the popup window is closed or cancel button is pressed, break the loop
        if popup_event == sg.WIN_CLOSED or popup_event == "Cancel":
            break

        # If the submit button is pressed, call the callback function with the entered text and break the loop
        if popup_event == "Submit":
            entered_text = popup_values["-TEXT-"]
            callback(parent_window, event, entered_text)
            break

    # Close the popup window
    popup_window.close()


def request_access(window, cropped_face, cap):
    block = sg.popup_get_text("Enter Block number")
    if block is not None:
        print(block)
        block = int(block)
        try:
            profile = Profile.objects.get(block_number=block)
            print(f"sent telegram msg to + {profile.user.username}")
        except:
            sg.popup_error("User does not exist")
