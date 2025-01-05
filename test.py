import io
import sys
import csv

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.QtGui import QColor

design = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Результат олимпиады: фильтрация</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QComboBox" name="schools">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>10</y>
      <width>121</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QComboBox" name="classes">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>10</y>
      <width>151</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="resultButton">
    <property name="geometry">
     <rect>
      <x>450</x>
      <y>10</y>
      <width>231</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <family>Microsoft JhengHei UI Light</family>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Узнать результаты</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>70</y>
      <width>801</width>
      <height>521</height>
     </rect>
    </property>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class OlympResult(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(design)
        uic.loadUi(f, self)  # Загружаем дизайн

        self.reader = []
        # Чтение CSV файла
        with open('rez.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            self.reader = [i for i in csv_reader]
        for i in ['Все'] + sorted({i['login'].split('-')[-3] for i in self.reader}, key=int):
            self.schools.addItem(str(i))
        for i in ['Все'] + sorted({i['login'].split('-')[-2] for i in self.reader}, key=int):
            self.classes.addItem(str(i))

        self.results = [[i['user_name'].split()[-2], i['Score']] for i in self.reader]
        first, second, third = [str(i) for i in sorted(set([int(i[1]) for i in self.results]), reverse=True)[:3]]
        self.tableWidget.setRowCount(len(self.results))
        self.tableWidget.setColumnCount(2)

        # Устанавливаем заголовки столбцов
        header_labels = ['Фамилия', 'Результат']
        self.tableWidget.setHorizontalHeaderLabels(header_labels)

        for i in range(len(self.results)):
            for j in range(2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(self.results[i][j]))
                if first == self.results[i][1]:
                    self.tableWidget.item(i, j).setBackground(QColor(204, 204, 0))
                elif second == self.results[i][1]:
                    self.tableWidget.item(i, j).setBackground(QColor(181, 181, 189))
                elif third == self.results[i][1]:
                    self.tableWidget.item(i, j).setBackground(QColor(156, 82, 33))

        self.resultButton.clicked.connect(self.act)
        self.schools.currentIndexChanged.connect(self.act1)

    def act(self):
        schools = self.schools.currentText()
        classes = self.classes.currentText()
        A = []
        if schools == 'Все' and classes != 'Все':
            A = [[i['user_name'].split()[-2], i['Score']] for i in self.reader if i['login'].split('-')[-2] == classes]
        elif schools != 'Все' and classes == 'Все':
            A = [[i['user_name'].split()[-2], i['Score']] for i in self.reader if i['login'].split('-')[-3] == schools]
        elif schools != 'Все' and classes != 'Все':
            A = [[i['user_name'].split()[-2], i['Score']] for i in self.reader if i['login'].split('-')[-3] == schools
                 and i['login'].split('-')[-2] == classes]
        else:
            A = self.results

        self.tableWidget.setRowCount(len(A))
        self.tableWidget.setColumnCount(2)

        # Устанавливаем заголовки столбцов
        header_labels = ['Фамилия', 'Результат']
        self.tableWidget.setHorizontalHeaderLabels(header_labels)

        first, second, third = [str(i) for i in (sorted(set([int(i[1]) for i in A]), reverse=True)[:3]
                                                 if len(sorted(set([int(i[1]) for i in A]), reverse=True)) > 2
                                                 else sorted(set([int(i[1]) for i in A]), reverse=True) +
                                [''] * (3 - len(sorted(set([int(i[1]) for i in A]),
                                                                             reverse=True))))]

        for i in range(len(A)):
            for j in range(2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(A[i][j]))
                if first == A[i][1]:
                    self.tableWidget.item(i, j).setBackground(QColor(204, 204, 0))
                elif second == A[i][1]:
                    self.tableWidget.item(i, j).setBackground(QColor(181, 181, 189))
                elif third == A[i][1]:
                    self.tableWidget.item(i, j).setBackground(QColor(156, 82, 33))

    def act1(self):
        self.classes.clear()
        if self.schools.currentText() == 'Все':
            for i in ['Все'] + sorted({i['login'].split('-')[-2] for i in self.reader}, key=int):
                self.classes.addItem(str(i))
        else:
            for i in ['Все'] + sorted({i['login'].split('-')[-2] for i in self.reader
                                       if i['login'].split('-')[-3] == self.schools.currentText()}, key=int):
                self.classes.addItem(str(i))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = OlympResult()
    program.show()
    sys.exit(app.exec())
