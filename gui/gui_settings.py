from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog, QTableWidgetItem, QTableWidget, QMainWindow, QPushButton

import os
import csv


def csv_init(table_widget):
    path = QFileDialog.getOpenFileName(table_widget, 'Open CSV', os.getenv('Diplom'), 'CSV(*.csv)')
    if path[0] != '':
        with open(path[0], encoding='UTF-8') as csv_file:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(30)
            my_file = csv.reader(csv_file)
            for row_data in my_file:
                row = table_widget.rowCount()
                table_widget.insertRow(row)
                if len(row_data) > 30:
                    table_widget.setColumnCount(len(row_data))
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    table_widget.setItem(row, column, item)


if __name__ == '__main__':
    csv_init()