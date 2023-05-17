#import typing
from PyQt5.QtWidgets import *
import sys, pickle

from PyQt5 import uic, QtWidgets, QtCore, QtGui
import data_visualize, table_display


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('./mainwindow.ui', self)

        global data
        data = data_visualize.data_()
        self.show()

        self.Browse = self.findChild(QPushButton, 'Browse')
        self.column_list = self.findChild(QListWidget, 'column_list')
        self.Submit_btn = self.findChild(QPushButton, 'Submit')
        self.target_col = self.findChild(QLabel, 'target_col')
        self.table = self.findChild(QTableView, 'tableView')
        self.data_shape = self.findChild(QLabel, 'shape')


        self.scaler = self.findChild(QComboBox, 'scaler')
        self.scale_btn = self.findChild(QPushButton, 'scale_btn')

        self.cat_column = self.findChild(QComboBox, 'cat_column')
        self.convert_btn = self.findChild(QPushButton, 'convert_btn')

        self.drop_column = self.findChild(QComboBox, 'drop_column')
        self.drop_btn = self.findChild(QPushButton, 'drop_btn')

        self.empty_column = self.findChild(QComboBox, 'empty_column')
        self.fillmean_btn = self.findChild(QPushButton, 'fillmean_btn')
        self.fillna_btn = self.findChild(QPushButton, 'fillna_btn')



        self.Browse.clicked.connect(self.getCSV)
        self.Submit_btn.clicked.connect(self.set_target)
        self.column_list.clicked.connect(self.target)

    def set_target(self):
        self.target_value = str(self.item).split()[0]
        print(self.target_value)
        self.target_col.setText(self.target_value)

    def target(self):
        self.item = self.column_list.currentItem().text()
        print(self.item)

    def getCSV(self):

        # 파일에 있는 절대 경로를 리턴(해당 파일이 어디에 있는지.)
        self.filepath , _ = QFileDialog.getOpenFileName(self, 'Opne File', "C:/Users/duja1/OneDrive/문서/GitHub/ubion_python_class_01/ml/datasets", 'csv(*.csv)') # csv 파일만 보이게 만듦
        # print(self.filepath)
        # self.column_list.clear()
        # self.column_list.addItems(['브라우져', '브라우승', '브라질'])
        self.filldetails(0)


    def fill_combo_box(self) :
        x = table_display.DataFrameModel(self.df)
        self.table.setModel(x)

    def filldetails(self, flag=1):
        import pandas as pd
        if (flag==0):
            self.df = data.read_file(self.filepath)

        self.column_list.clear()
       
        if len(self.df) == 0 :
            pass
        else :
            self.column_arr = data.get_column_list(self.df)
            # print(self.column_arr)
            for i, j in enumerate(self.column_arr):
                stri = f'{j} ------- {str(self.df[j].dtype)}'
                self.column_list.insertItem(i,stri)

        df_shape = f"Shape-rows : {self.df.shape[0]}, columns : {self.df.shape[1]}"
        self.data_shape.setText(df_shape)
        self.fill_combo_box()

# 가장 먼저 실행 시키고 싶은거를 갖다가 넣으면 됨
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #self.show()
    window = UI()
    app.exec_()
