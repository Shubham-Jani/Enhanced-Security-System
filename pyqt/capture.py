import os
import sys
sys.path.append('/media/data_s/Programs/vvp_hackathon/webapp')
from django_setup import *
import numpy as np
import face_recognition
import cv2
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from userprofile.models import Profile
from django.contrib.auth.models import User




# Set up Django environment


class Ui_MainWindow(object):
    is_recording = False

    # set up the face recognition variables

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.webCamFeed = QtWidgets.QLabel(self.centralwidget)
        self.webCamFeed.setGeometry(QtCore.QRect(20, 30, 481, 361))
        self.webCamFeed.setAutoFillBackground(False)
        self.webCamFeed.setStyleSheet(
            "border-style:solid;\n"
            "border-width:5;\n"
            "border-color:brown;")
        self.webCamFeed.setTextFormat(QtCore.Qt.RichText)
        self.webCamFeed.setAlignment(QtCore.Qt.AlignCenter)
        self.webCamFeed.setObjectName("webCamFeed")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(530, 30, 221, 112))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.DateTimeGrid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.DateTimeGrid.setContentsMargins(0, 0, 0, 0)
        self.DateTimeGrid.setObjectName("DateTimeGrid")
        self.timeLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans Display")
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.timeLabel.setFont(font)
        self.timeLabel.setTextFormat(QtCore.Qt.RichText)
        self.timeLabel.setObjectName("timeLabel")
        self.DateTimeGrid.addWidget(self.timeLabel, 1, 0, 1, 1)
        self.dateLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans Display")
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.dateLabel.setFont(font)
        self.dateLabel.setTextFormat(QtCore.Qt.RichText)
        self.dateLabel.setObjectName("dateLabel")
        self.DateTimeGrid.addWidget(self.dateLabel, 0, 0, 1, 1)
        self.date = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans Display")
        font.setPointSize(22)
        self.date.setFont(font)
        self.date.setTextFormat(QtCore.Qt.AutoText)
        self.date.setObjectName("date")
        self.DateTimeGrid.addWidget(self.date, 0, 1, 1, 1)
        self.time = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans Display")
        font.setPointSize(22)
        self.time.setFont(font)
        self.time.setObjectName("time")
        self.DateTimeGrid.addWidget(self.time, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(510, 160, 271, 371))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 40, 231, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.name = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.blockLabel = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.blockLabel.setObjectName("blockLabel")
        self.gridLayout.addWidget(self.blockLabel, 1, 0, 1, 1)
        self.block = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.block.setObjectName("block")
        self.gridLayout.addWidget(self.block, 1, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 450, 88, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushButton_clicked)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.known_face_encodings = []
        self.known_face_names = []
        users = User.objects.all()
        # faces = Face.objects.all()
        for user in users:
            if user.is_staff:
                continue
            face_encodings = np.frombuffer(user.profile.face_encodings)
            self.known_face_encodings.append(face_encodings)
            self.known_face_names.append(user.username)
        # print(len(self.known_face_encodings))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.webCamFeed.setText(_translate("MainWindow", "Image"))
        self.timeLabel.setText(_translate("MainWindow", "Time:"))
        self.dateLabel.setText(_translate("MainWindow", "Date:"))
        self.date.setText(_translate(
            "MainWindow", str(datetime.datetime.now())))
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time.setText(_translate("MainWindow", current_time))
        self.groupBox.setTitle(_translate("MainWindow", "Details"))
        self.name.setText(_translate("MainWindow", "wtf"))
        self.nameLabel.setText(_translate("MainWindow", "Name:"))
        self.blockLabel.setText(_translate("MainWindow", "Block:"))
        self.block.setText(_translate("MainWindow", "-"))
        self.pushButton.setText(_translate("MainWindow", "start"))

    def pushButton_clicked(self):
        if not self.is_recording:
            # create a timer to update the video stream
            self.pushButton.setText("Stop Recording")
            self.is_recording = True
            self.capture = cv2.VideoCapture(1)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)
        else:
            self.pushButton.setText("Start Recording")
            self.is_recording = False
            self.timer.stop()
            self.capture.release()

    def update_frame(self):
        # read a frame from the webcam
        if not self.capture.isOpened():
            print("Could not open webcam.")
            return

        ret, frame = self.capture.read()
        # frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # self.capture.set(cv2.CAP_PROP_FPS, 15)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 140)
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            frame, face_locations)
        if ret:

            # convert the frame to RGB image
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, face_encoding, tolerance=0.5)
                print(matches)
                if True in matches:
                    first_match_index = matches.index(True)
                    # name = self.knownusers[first_match_index+1]["username"]
                    print(first_match_index)
                    name = self.known_face_names[first_match_index]
                    cv2.putText(frame, name, (left + 6, bottom - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
                    # self.resident_name.setText(name)
                    # self.resident_block.setText(
                    #     str(self.users[first_match_index+1]["profile"]["block_number"]))
                    # self.record_button.setText("Start Recording")
                    name = self.known_face_names[0]
                    self.is_recording = False
                    self.timer.stop()
                    self.capture.release()

                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # create a QImage from the RGB image
            qimage = QImage(
                rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format.Format_RGB888)

            # create a QPixmap from the QImage
            pixmap = QPixmap.fromImage(qimage)

            # set the QPixmap to the QLabel
            self.webCamFeed.setPixmap(pixmap)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
