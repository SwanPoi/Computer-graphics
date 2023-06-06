# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt


class MyGraphicsView(QGraphicsView):
    cnt_calls_resizeEvent = 0
    cnt_zoom = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.image = QImage(5000, 5000, QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)
        self.cnt_calls_resizeEvent = 0
        self.cnt_zoom = 0

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        scale_factor = 1.5

        if event.angleDelta().y() > 0:
            self.scale(scale_factor, scale_factor)
            self.cnt_zoom += 1
        elif self.cnt_zoom != 0:
            self.scale(1 / scale_factor, 1 / scale_factor)
            self.cnt_zoom -= 1


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(927, 728)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(300, 167000))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 2)
        self.points_tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.points_tableWidget.setObjectName("points_tableWidget")
        self.points_tableWidget.setColumnCount(0)
        self.points_tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.points_tableWidget, 1, 0, 1, 4)
        self.cut_tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.cut_tableWidget.setObjectName("cut_tableWidget")
        self.cut_tableWidget.setColumnCount(0)
        self.cut_tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.cut_tableWidget, 1, 4, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 6)
        self.x_label = QtWidgets.QLabel(self.groupBox)
        self.x_label.setObjectName("x_label")
        self.gridLayout.addWidget(self.x_label, 3, 0, 1, 1)
        self.x_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.x_lineEdit.setObjectName("x_lineEdit")
        self.gridLayout.addWidget(self.x_lineEdit, 3, 1, 1, 2)
        self.y_label = QtWidgets.QLabel(self.groupBox)
        self.y_label.setObjectName("y_label")
        self.gridLayout.addWidget(self.y_label, 3, 3, 1, 1)
        self.y_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.y_lineEdit.setObjectName("y_lineEdit")
        self.gridLayout.addWidget(self.y_lineEdit, 3, 4, 1, 2)
        self.add_point_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.add_point_pushButton.setObjectName("add_point_pushButton")
        self.gridLayout.addWidget(self.add_point_pushButton, 4, 0, 1, 6)
        self.xl_label = QtWidgets.QLabel(self.groupBox)
        self.xl_label.setObjectName("xl_label")
        self.gridLayout.addWidget(self.xl_label, 5, 0, 1, 2)
        self.x_left_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.x_left_lineEdit.setObjectName("x_left_lineEdit")
        self.gridLayout.addWidget(self.x_left_lineEdit, 5, 2, 1, 2)
        self.yl_label = QtWidgets.QLabel(self.groupBox)
        self.yl_label.setObjectName("yl_label")
        self.gridLayout.addWidget(self.yl_label, 5, 4, 1, 1)
        self.y_left_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.y_left_lineEdit.setObjectName("y_left_lineEdit")
        self.gridLayout.addWidget(self.y_left_lineEdit, 5, 5, 1, 1)
        self.xr_label = QtWidgets.QLabel(self.groupBox)
        self.xr_label.setObjectName("xr_label")
        self.gridLayout.addWidget(self.xr_label, 6, 0, 1, 2)
        self.x_right_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.x_right_lineEdit.setObjectName("x_right_lineEdit")
        self.gridLayout.addWidget(self.x_right_lineEdit, 6, 2, 1, 2)
        self.yr_label = QtWidgets.QLabel(self.groupBox)
        self.yr_label.setObjectName("yr_label")
        self.gridLayout.addWidget(self.yr_label, 6, 4, 1, 1)
        self.y_right_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.y_right_lineEdit.setObjectName("y_right_lineEdit")
        self.gridLayout.addWidget(self.y_right_lineEdit, 6, 5, 1, 1)
        self.add_cut_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.add_cut_pushButton.setObjectName("add_cut_pushButton")
        self.gridLayout.addWidget(self.add_cut_pushButton, 7, 0, 1, 6)
        self.final_cut_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.final_cut_pushButton.setObjectName("final_cut_pushButton")
        self.gridLayout.addWidget(self.final_cut_pushButton, 8, 0, 1, 6)
        self.color_cut_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.color_cut_pushButton.setObjectName("color_cut_pushButton")
        self.gridLayout.addWidget(self.color_cut_pushButton, 9, 0, 1, 4)
        self.color_cut_label = QtWidgets.QLabel(self.groupBox)
        self.color_cut_label.setText("")
        self.color_cut_label.setObjectName("color_cut_label")
        self.gridLayout.addWidget(self.color_cut_label, 9, 4, 1, 2)
        self.color_segment_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.color_segment_pushButton.setObjectName("color_segment_pushButton")
        self.gridLayout.addWidget(self.color_segment_pushButton, 10, 0, 1, 4)
        self.color_segment_label = QtWidgets.QLabel(self.groupBox)
        self.color_segment_label.setText("")
        self.color_segment_label.setObjectName("color_segment_label")
        self.gridLayout.addWidget(self.color_segment_label, 10, 4, 1, 2)
        self.color_final_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.color_final_pushButton.setObjectName("color_final_pushButton")
        self.gridLayout.addWidget(self.color_final_pushButton, 11, 0, 1, 4)
        self.color_final_label = QtWidgets.QLabel(self.groupBox)
        self.color_final_label.setText("")
        self.color_final_label.setObjectName("color_final_label")
        self.gridLayout.addWidget(self.color_final_label, 11, 4, 1, 2)
        self.cut_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.cut_pushButton.setObjectName("cut_pushButton")
        self.gridLayout.addWidget(self.cut_pushButton, 12, 0, 1, 6)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.graphicsView = MyGraphicsView(self.centralwidget)
        self.graphicsView.setMaximumSize(QtCore.QSize(1677000, 1677000))
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 927, 26))
        self.menubar.setObjectName("menubar")
        self.program_menu = QtWidgets.QMenu(self.menubar)
        self.program_menu.setObjectName("program_menu")
        self.author_menu = QtWidgets.QMenu(self.menubar)
        self.author_menu.setObjectName("author_menu")
        self.clear_menu = QtWidgets.QMenu(self.menubar)
        self.clear_menu.setObjectName("clear_menu")
        self.exit_menu = QtWidgets.QMenu(self.menubar)
        self.exit_menu.setObjectName("exit_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.program_menu.menuAction())
        self.menubar.addAction(self.author_menu.menuAction())
        self.menubar.addAction(self.clear_menu.menuAction())
        self.menubar.addAction(self.exit_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Введенные отрезки"))
        self.label_3.setText(_translate("MainWindow", "Введенный отсекатель"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p>ЛКМ №1 - левая верхняя точка отсекателя</p><p>ЛКМ №2 - правая нижняя точка отсекателя</p><p>ПКМ - добавление точки отрезка</p></body></html>"))
        self.x_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">X:</span></p></body></html>"))
        self.y_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Y:</span></p></body></html>"))
        self.add_point_pushButton.setText(_translate("MainWindow", "Добавить точку отрезка"))
        self.xl_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Xлв:</span></p></body></html>"))
        self.yl_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Yлв:</span></p></body></html>"))
        self.xr_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Xпн:</span></p></body></html>"))
        self.yr_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Yпн:</span></p></body></html>"))
        self.add_cut_pushButton.setText(_translate("MainWindow", "Добавить отсекатель"))
        self.final_cut_pushButton.setText(_translate("MainWindow", "Замкнуть фигуру"))
        self.color_cut_pushButton.setText(_translate("MainWindow", "Цвет отсекателя"))
        self.color_segment_pushButton.setText(_translate("MainWindow", "Цвет отрезков"))
        self.color_final_pushButton.setText(_translate("MainWindow", "Цвет отсеченного"))
        self.cut_pushButton.setText(_translate("MainWindow", "Произвести отсечение"))
        self.program_menu.setTitle(_translate("MainWindow", "О программе"))
        self.author_menu.setTitle(_translate("MainWindow", "Об авторе"))
        self.clear_menu.setTitle(_translate("MainWindow", "Очистка"))
        self.exit_menu.setTitle(_translate("MainWindow", "Выход"))