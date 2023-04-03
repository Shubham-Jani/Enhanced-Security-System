# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'untitledJOlbMA.ui'
##
# Created by: Qt User Interface Compiler version 5.15.8
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1139, 868)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.calendarWidget = QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setGeometry(QRect(810, 0, 321, 191))
        self.timeEdit = QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(810, 200, 123, 32))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(30, 60, 751, 701))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.nameLabel = QLabel(self.centralwidget)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setGeometry(QRect(810, 250, 101, 31))
        self.blockLabel = QLabel(self.centralwidget)
        self.blockLabel.setObjectName(u"blockLabel")
        self.blockLabel.setGeometry(QRect(810, 300, 58, 18))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1139, 30))
        self.menuShow = QMenu(self.menubar)
        self.menuShow.setObjectName(u"menuShow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuShow.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
        self.nameLabel.setText(
            QCoreApplication.translate("MainWindow", u"Name", None))
        self.blockLabel.setText(
            QCoreApplication.translate("MainWindow", u"Block", None))
        self.menuShow.setTitle(
            QCoreApplication.translate("MainWindow", u"Show", None))
    # retranslateUi
