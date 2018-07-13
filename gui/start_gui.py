from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog, QTableWidgetItem, QTableWidget, QMainWindow, QPushButton

import os
import csv
import gui.gui_settings as settings
import multiprocessing as multi

from gui.main_gui import Ui_MainWindow
from twitter.twitter import AppTwitter
from instagram.main_inst import AppInsta
from vk.vk_user import VkMain
from linkedin.main_linken import LinkenApp


class GuiMain(Ui_MainWindow):
    def main(self):
        self.pushButton_3.clicked.connect(self.init_table_tw)
        self.pushButton_4.clicked.connect(self.init_table_inst)
        self.pushButton_7.clicked.connect(self.init_table_vk)
        self.pushButton_10.clicked.connect(self.init_table_ld)

        self.pushButton.clicked.connect(self.button_clicked_tw)
        self.pushButton_6.clicked.connect(self.button_clicked_inst)
        self.pushButton_9.clicked.connect(self.button_clicked_vk)
        self.pushButton_12.clicked.connect(self.button_clicked_ld)

    def button_clicked_tw(self):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        parse_name = self.lineEdit_5.text()

        return AppTwitter(name, password, parse_name)

    def button_clicked_inst(self):
        name = self.lineEdit_4.text()
        password = self.lineEdit_3.text()
        parse_name = self.lineEdit_6.text()

        return AppInsta(name, password, parse_name)

    def button_clicked_vk(self):
        parse_name = self.lineEdit_9.text()

        return VkMain(parse_name)

    def button_clicked_ld(self):
        name = self.lineEdit_8.text()
        password = self.lineEdit_7.text()
        parse_name = self.lineEdit_10.text()

        return LinkenApp(password, name, parse_name)


    def init_table_tw(self):
        table_widget = self.tableWidget
        settings.csv_init(table_widget)

    def init_table_inst(self):
        table_widget = self.tableWidget_2
        settings.csv_init(table_widget)

    def init_table_vk(self):
        table_widget = self.tableWidget_3
        settings.csv_init(table_widget)

    def init_table_ld(self):
        table_widget = self.tableWidget_4
        settings.csv_init(table_widget)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GuiMain()
    ui.setupUi(MainWindow)
    ui.main()
    MainWindow.show()
    sys.exit(app.exec_())
