from PyQt5.QtWidgets import * 
import sys , pickle

from PyQt5 import uic, QtWidgets , QtCore, QtGui
import data_visualize , table_display
import Linear_Regression, SVM, Logistic_Regression, Random_Forest

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("./mainwindow.ui", self)
        
        global data
        data  = data_visualize.data_()
        self.show()
        self.target_value =''
        
        self.Browse = self.findChild( QPushButton, "Browse" )
        self.column_list = self.findChild( QListWidget, "column_list" )
        self.Submit_btn = self.findChild( QPushButton, "Submit" )
        self.target_col = self.findChild( QLabel, "target_col" )
        self.table = self.findChild( QTableView, "tableView" )
        self.data_shape = self.findChild( QLabel, "shape" )
        self.Nontarget_alarm = self.findChild( QLabel, "Nontarget_alarm" )
        
        self.scaler = self.findChild( QComboBox, "scaler" )
        self.scale_btn = self.findChild( QPushButton, "scale_btn" )
        
        self.cat_column = self.findChild( QComboBox, "cat_column" )
        self.convert_btn = self.findChild( QPushButton, "convert_btn" )
        
        self.drop_column = self.findChild( QComboBox, "drop_column" )
        self.drop_btn = self.findChild( QPushButton, "drop_btn" )
        
        self.empty_column = self.findChild( QComboBox, "empty_column" )
        self.fillmean_btn = self.findChild( QPushButton, "fillmean_btn" )
        self.fillna_btn = self.findChild( QPushButton, "fillna_btn" )

        # scatter plot
        self.scatter_x = self.findChild( QComboBox, "scatter_x" )
        self.scatter_y = self.findChild( QComboBox, "scatter_y" )
        self.scatter_c = self.findChild( QComboBox, "scatter_c" )
        self.scatter_marker = self.findChild( QComboBox, "scatter_marker" )
        self.scatterplot = self.findChild(QPushButton,"scatterplot")

        # line plot
        self.plot_x = self.findChild( QComboBox, "plot_x" )
        self.plot_y = self.findChild( QComboBox, "plot_y" )
        self.plot_c = self.findChild( QComboBox, "plot_c" )
        self.plot_marker = self.findChild( QComboBox, "plot_marker" )
        self.lineplot = self.findChild(QPushButton,"lineplot")

        # model training ui
        self.model_select = self.findChild( QComboBox, "model_select" )
        self.train = self.findChild(QPushButton,"train")

        self.train.clicked.connect(self.train_func)
        self.scatterplot.clicked.connect(self.scatter_plot)
        self.lineplot.clicked.connect(self.line_plot)

        self.Browse.clicked.connect(self.getCSV)
        self.Submit_btn.clicked.connect(self.set_target)
        self.column_list.clicked.connect(self.target)
        self.convert_btn.clicked.connect(self.convert_cat)
        self.drop_btn.clicked.connect(self.dropc)
        
        self.fillmean_btn.clicked.connect(self.fillme)
        self.fillna_btn.clicked.connect(self.fillna)
        self.scale_btn.clicked.connect(self.scale_value)

    def train_func(self) :
        my_dict = {"Linear Regression" : Linear_Regression,
                   "SVM" : SVM,
                   "Logistic Regression" : Logistic_Regression,
                   "Random Forest" : Random_Forest}
        
        if self.target_value !='' :
            name = self.model_select.currentText()
            self.win = my_dict[name].UI(self.df, self.target_value)

    def line_plot(self) :
        x = self.plot_x.currentText()
        y = self.plot_y.currentText()
        c = self.plot_c.currentText()
        marker = self.plot_marker.currentText()
        data.line_graph(df=self.df, x=x, y=y, c=c, marker = marker)


    def scatter_plot(self):
        x = self.scatter_x.currentText()
        y = self.scatter_y.currentText()
        c = self.scatter_c.currentText()
        marker = self.scatter_marker.currentText()
        data.scatter_graph(df=self.df, x=x, y=y, c=c, marker = marker)

    def scale_value(self) :
        if self.scaler.currentText() == "StandardScaler" :
            self.df = data.StandardScaler(self.df, self.target_value)

        elif self.scaler.currentText() == "MinMaxScaler" :
            self.df = data.MinMaxScaler(self.df, self.target_value)

        elif self.scaler.currentText() == "PowerScaler" :
            self.df = data.PowerScaler(self.df, self.target_value)

        self.filldetails()
        
    def fillna(self):
        name = self.empty_column.currentText()
        self.df[name] = data.fillnan(self.df , name)
        self.filldetails()
        
    def fillme(self):
        name = self.empty_column.currentText()
        self.df[name] = data.fillmean(self.df , name)
        self.filldetails()
        
    def dropc(self):
        name = self.drop_column.currentText()
        if self.target_value == '':
            self.Nontarget_alarm.setText('please setTarget!!!')
        else:
            if ( name == self.target_value):
                pass
            
            else:
                self.df = data.drop_columns(self.df,name)
                self.filldetails()
    
    def convert_cat(self):
        name = self.cat_column.currentText()
        self.df[name] = data.convert_category(self.df, name)
        self.filldetails()
    
    def set_target(self):
        self.Nontarget_alarm.setText('')
        self.target_value = str(self.item).split()[0]
        print(self.target_value)
        self.target_col.setText(self.target_value)
        
    def target(self):
        self.item = self.column_list.currentItem().text()
        print(self.item)
        
    def getCSV(self):
        self.filepath , _ = QFileDialog.getOpenFileName(self,"Open File", "C:/Users/duja1/OneDrive/문서/GitHub/ubion_python_class_01/ml/datasets","csv(*.csv)" )
        # print(self.filepath)
        # self.column_list.addItems(["브라우져", '브라우승', "브라질"])
        self.filldetails(0)          
    
    def fill_combo_box(self):
        
        self.cat_column.clear()
        self.cat_column.addItems(self.cat_col_list)
        
        self.drop_column.clear()
        self.drop_column.addItems(self.column_arr)
        
        self.empty_column.clear()
        self.empty_column.addItems(self.empty_column_name)

        self.scatter_x.clear()
        self.scatter_x.addItems(self.column_arr) 

        self.scatter_y.clear()
        self.scatter_y.addItems(self.column_arr)

        self.plot_x.clear()
        self.plot_x.addItems(self.column_arr) 

        self.plot_y.clear()
        self.plot_y.addItems(self.column_arr)

        x = table_display.DataFrameModel(self.df)
        self.table.setModel(x)
        
    def filldetails(self , flag=1):
        if (flag==0):
            self.df = data.read_file(self.filepath)
            # print(self.df)
            
        self.column_list.clear()    
        self.cat_col_list = data.get_cat(self.df)
        self.empty_column_name=data.get_empty_list(self.df)
        
        if len(self.df)==0:
            pass
            
        else:
            
            self.column_arr = data.get_column_list(self.df)
            # print(self.column_arr)
            for i , j in enumerate(self.column_arr):
                stri = f'{j} ------- {str(self.df[j].dtype)}'
                self.column_list.insertItem(i, stri)
        
            df_shape = f'Shape-rows :{self.df.shape[0]} , columns:{self.df.shape[1]}'
            self.data_shape.setText(df_shape)
        
        
            self.fill_combo_box()
        

if __name__ == '__main__':       
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()