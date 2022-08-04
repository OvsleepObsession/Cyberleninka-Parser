# -*- coding: utf-8 -*-
"""
Обработка GUI
Написано : Чернецкий Андрей, БИВ174
"""
from PyQt5 import QtWidgets, QtCore, QtGui
from kurs_gui import Ui_MainWindow  
from No_Internet import Ui_Dialog
import sys
import kurs
import webbrowser
from pathlib import Path

 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.on_push_button_click)
        self.ui.pushButton_2.clicked.connect(self.on_push_button_2_click)
        self.ui.tableWidget.itemDoubleClicked.connect(self.OpenLink)

    def OpenLink(self, item):
        if item.column() == 1:
            webbrowser.open(self.ui.tableWidget.item(item.row(), item.column()).text())
        
    def addcolumn(self, link, tytle, author, description):
        rowCnt = self.ui.tableWidget.rowCount()
        app.processEvents()
        font = QtGui.QFont()
        font.setUnderline(True)
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        checkbox = self.create_checkbox_for_table()
        self.ui.tableWidget.setCellWidget(rowCnt, 0, checkbox)
        self.ui.tableWidget.setItem(rowCnt, 1, QtWidgets.QTableWidgetItem(link))
        self.ui.tableWidget.item(rowCnt, 1).setFont(font)
        self.ui.tableWidget.item(rowCnt, 1).setData(QtCore.Qt.TextColorRole, QtGui.QColor(30, 150, 250))
        self.ui.tableWidget.setItem(rowCnt, 2, QtWidgets.QTableWidgetItem(tytle))
        self.ui.tableWidget.setItem(rowCnt, 3, QtWidgets.QTableWidgetItem(author))
        self.ui.tableWidget.setItem(rowCnt, 4, QtWidgets.QTableWidgetItem(description))
        self.ui.tableWidget.resizeRowsToContents()
    
    def nointernet(self, Dialog):
         self.ui2 = Ui_Dialog()
         self.ui2.setupUi(Dialog)
         Dialog.show()
         
    def fixfilename(self, st):
        sr = ""
        for i in range(len(st)):
            if (st[i] != ":") and (st[i] != "?") and (st[i] != "/") and (st[i] != "\\") and (st[i] != "*") and (st[i] != "<") and (st[i] != ">") and (st[i] != "\"") and (st[i] != "|"):
                sr = sr + st[i]
        return sr
    
    def checkinternet(self):
        try:
            kurs.urllib.request.urlopen("http://google.com")
            return True
        except IOError:
            return False

    def create_checkbox_for_table(self):
         pWidget = QtWidgets.QWidget()  
         pCheckBox = QtWidgets.QCheckBox() 
         pLayout = QtWidgets.QHBoxLayout(pWidget)
         pLayout.addWidget(pCheckBox) 
         pLayout.setAlignment(QtCore.Qt.AlignCenter)
         pLayout.setContentsMargins(0,0,0,0) 
         pWidget.setLayout(pLayout)
         return pWidget  
            

    def on_push_button_2_click(self):
        if self.checkinternet() == False:
            self.nointernet(Dialog)
            return
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(
            (' ', 'Link', 'Article name', 'Authors', 'Description')
        )
        self.ui.tableWidget.setRowCount(0);
        enter = self.ui.lineEdit.text()
        kurs.pars(self, enter)
        self.ui.progress.setValue(100)
    def on_push_button_click(self):
        if self.ui.lineEdit_2.text() == "":
            self.ui.lineEdit_2.setStyleSheet("border: 2px solid red;")
            return
        self.ui.lineEdit_2.setStyleSheet("border: 1px solid black;")
        rowCnt = self.ui.tableWidget.rowCount()
        for i in range(rowCnt):
            if self.ui.tableWidget.cellWidget(i, 0).findChild(type(QtWidgets.QCheckBox())).isChecked():
                url= self.ui.tableWidget.item(i, 1).text()
                html_doc = kurs.urllib.request.urlopen(url)
                url = kurs.BeautifulSoup(html_doc, 'html.parser').find('meta', {'name' : 'citation_pdf_url'}).get('content')
                u = self.ui.lineEdit_2.text()
                if Path(u).exists() == False:
                    self.ui.lineEdit_2.setStyleSheet("border: 2px solid red;")
                    return
                else:
                    self.ui.lineEdit_2.setStyleSheet("border: 1px solid black;")
                    kurs.urllib.request.urlretrieve(url, u + "/" + self.fixfilename(self.ui.tableWidget.item(i, 2).text()) + ".pdf")


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
Dialog = QtWidgets.QDialog()
sys.exit(app.exec())