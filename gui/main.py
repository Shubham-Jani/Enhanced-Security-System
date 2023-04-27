import datetime
import cv2
import PySimpleGUI as sg
import numpy as np
import face_recognition
from util import *
import time

resident_frame = [sg.Frame('Details: ', [
    [sg.Image(key='-FACE-')],
    [sg.Text("Name:"), sg.Text(key='-NAME-')],
    [sg.Text("Block Number:"), sg.Text(key='-BLOCK-')]])]

visitor_frame = [
    sg.Frame('Request Access',
             [
                 [sg.Text('Enter the block no. you want to visit:')],
                 [sg.InputText(key='-BLOCK-', disabled=True)],
                 [sg.Button('Submit', disabled=True), sg.Button('Cancel', disabled=True)]],
             key="-VISITOR_FRAME-")
]


layout = [
    [sg.Frame('Camera Feed', [[sg.Image(key='-IMAGE-')]]),
     sg.Frame('', [
         [sg.Frame('Date and Time', [[sg.Text("Date:"), sg.Text(key="-DATE-")],
                                     [sg.Text("Time"), sg.Text(key="-TIME-")]]),],
         [sg.Frame('Details: ', [
                                [sg.Image(key='-FACE-')],
                                [sg.Text("Name:"), sg.Text(key='-NAME-')],
             [sg.Text("Block Number:"), sg.Text(key='-BLOCK-')]],
             key="-DETAILS_FRAME-")]
     ])
     ],
    [sg.Button('Exit'), sg.Button('STOP/Start', key="-REC-")]
]

window = sg.Window("Admin", layout)
known_face_encodings, known_face_ids = get_stored_encodings()

cap = cv2.VideoCapture(1)

while True:
    # window["-VISITOR_FRAME-"].update(disabled=True)
    event, values = window.read(timeout=20)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    ret, frame = cap.read()

    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)

    name, block, ids = recognize_faces(
        frame, face_locations, known_face_encodings, known_face_ids)

    is_resident, cropped_face = update_gui(
        window, frame, face_locations, name, block)
    update_date_time(window)
    if (is_resident):
        open_gate(window, event, ids, cropped_face, cap)
    else:
        if cropped_face == None:
            pass
        else:
            # sg.popup("Hello, World!", title="Popup Window")
            request_access(window, cropped_face, cap)


cap.release()
window.close()
