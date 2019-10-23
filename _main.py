#✏✏✏✏✏✏✐✐✐✐✎✎✎✎✒✒✒✒✑✑✑✑✑✉✉✉✉
import sys
import os
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sqlalchemy import create_engine
from sqlalchemy import Table, Column,VARCHAR,INTEGER,Float,String, MetaData,ForeignKey,Date,Text
from sqlalchemy.sql import exists
import subprocess
import sqlconn as sqc






ui, _ = loadUiType('Payroll_System.ui')
ui2, _ = loadUiType('Add_Employee.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()

    def Handle_UI_Changes(self):
        self.login_logo_button.setEnabled(False)
        self.login_design_button.setEnabled(False)
        self.home_logo.setEnabled(False)
        self.home_design.setEnabled(False)
        self.payroll_home_logo.setEnabled(False)
        self.payroll_home_image.setEnabled(False)
        self.payroll_home_design.setEnabled(False)
        self._container.setVisible(False)
        self.payroll_view_table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.payroll_ae_table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.payslip_tab_widget.tabBar().setVisible(False)
        self.payslip_tab_widget.setCurrentIndex(0)



    def Handle_Buttons(self):
        self.login_button.clicked.connect(self.login_button_action)
        self._home_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self._payroll_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.payroll_home_new.clicked.connect(self.payroll_home_new_action)
        self.payroll_home_edit.clicked.connect(self.payroll_home_edit_action)
        self.payroll_home_view.clicked.connect(self.payroll_home_view_action)
        self.payroll_view_quit.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.payroll_ae_add_person.clicked.connect(self.payroll_ae_add_person_action)
        self.payroll_ae_quit.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self._payslip_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(5))
        self._quit_button.clicked.connect(self._quit_button_action)
        self._settings_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(6))
        self.settings_table_widget_signatory.resizeColumnsToContents()


    def _quit_button_action(self):
        self.login_warning.setText(' ')
        self.tabWidget.setCurrentIndex(0)
        self._container.setVisible(False)




    def login_button_action(self):
        username = self.login_username.text()
        password = self.login_password.text()

        engine = sqc.Database().engine
        payroll_admin = sqc.Database().payroll_admin

        conn = engine.connect()
        s = payroll_admin.select()
        s_value = conn.execute(s)


        for val in s_value:
            if str(username).lower() == str(val[1]).lower() and str(password).lower() == str(val[2]).lower():
                if val[3] == 'admin':
                    self.tabWidget.setCurrentIndex(1)
                    self._container.setVisible(True)
                    self._home_button.setVisible(True)
                    self._payroll_button.setVisible(True)
                    self._settings_button.setVisible(True)
                elif val[3] == 'user':
                    self.tabWidget.setCurrentIndex(1)
                    self._container.setVisible(True)
                    self._home_button.setVisible(True)
                    self._payroll_button.setVisible(False)
                    self._settings_button.setVisible(False)

            else:
                self.login_warning.setText('Wrong Username or Password.')

        self.login_username.setText('')
        self.login_password.setText('')


        if username == 'admin' and password == 'admin':
            self.tabWidget.setCurrentIndex(1)
            self._container.setVisible(True)
        else:
            self.login_warning.setText('Wrong Username or Password.')

    def payroll_home_new_action(self):
        self.tabWidget.setCurrentIndex(4)


    def payroll_home_edit_action(self):
        self.tabWidget.setCurrentIndex(4)


    def payroll_home_view_action(self):
        self.tabWidget.setCurrentIndex(3)

    def payroll_ae_add_person_action(self):
        dialog = Add_Employee_Dialogue(self)
        dialog.show()









class Add_Employee_Dialogue(QDialog,ui2):
    def __init__(self,parent=None):
        super(Add_Employee_Dialogue,self).__init__(parent)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Button_Changes()

    def Handle_UI_Changes(self):
        pass
    def Handle_Button_Changes(self):
        pass



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

