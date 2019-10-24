#✏✏✏✏✏✏✐✐✐✐✎✎✎✎✒✒✒✒✑✑✑✑✑✉✉✉✉
import sys
import os
from PyQt5 import QtCore,QtGui,QtWidgets,uic
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
import datetime
##globals
global settings_table_widget_accounts
global settings_table_widget_salary_grade
global settings_table_widget_signatory
global payroll_home_list_dict
global payroll_home_list_widget



main_ui, _ = loadUiType('Payroll_System.ui')
add_payroll_ui, _ = loadUiType('Add_Payroll.ui')
add_employee_ui, _ = loadUiType('Add_Employee.ui')
accounts_ui, _ = loadUiType('Accounts.ui')
designation_ui, _ = loadUiType('Designation.ui')
signatories_ui, _ = loadUiType('Signatories.ui')




class MainApp(QMainWindow, main_ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()
        self.Default_Text()



    def Default_Text(self):
        self.login_title.setText('PHRMO Payroll Information System')
        self.home_title.setText('PHRMO Payroll Information System')
        self.home_text.setText('This System is created as a Capstone Project from Sorsogon State College 2019 ©')
        self.payroll_home_title.setText('Payroll Record')
        self.settings_account_title.setText('Accounts')
        self.settings_salary_grade_title.setText('Salary Grade')
        self.settings_signatory_title.setText('Signatory')
        self.payslip_title.setText('Employee Payslip Records')
        pass


    def Handle_UI_Changes(self):
        ##globals
        global settings_table_widget_accounts
        global settings_table_widget_salary_grade
        global settings_table_widget_signatory
        global payroll_home_list_widget
        ##main
        self._container.setVisible(False)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        ##login
        self.login_logo_button.setEnabled(False)
        self.login_design_button.setEnabled(False)
        ##home
        self.home_logo.setEnabled(False)
        self.home_design.setEnabled(False)
        ##payroll_home
        payroll_home_list_widget = self.payroll_home_list_widget
        self.payroll_home_logo.setEnabled(False)
        self.payroll_home_image.setEnabled(False)
        self.payroll_home_design.setEnabled(False)
        ##payroll_view
        self.payroll_view_table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        ##payroll_ae
        self.payroll_ae_table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        ##payslip
        self.payslip_logo_1.setEnabled(False)
        self.payslip_logo_2.setEnabled(False)
        self.payslip_tab_widget.tabBar().setVisible(False)
        self.payslip_tab_widget.setCurrentIndex(0)
        ##settings
        self.show_settings()
        self.settings_table_widget_accounts.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_table_widget_salary_grade.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_table_widget_signatory.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_table_widget_accounts.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.settings_table_widget_salary_grade.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.settings_table_widget_signatory.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        #self.settings_table_widget_accounts.resizeColumnsToContents()
        #self.settings_table_widget_salary_grade.resizeColumnsToContents()
        self.settings_table_widget_signatory.resizeColumnsToContents()
        self.settings_table_widget_accounts.setColumnHidden(0,True)
        self.settings_table_widget_salary_grade.setColumnHidden(0,True)
        self.settings_table_widget_signatory.setColumnHidden(0,True)
        settings_table_widget_accounts = self.settings_table_widget_accounts
        settings_table_widget_salary_grade = self.settings_table_widget_salary_grade
        settings_table_widget_signatory = self.settings_table_widget_signatory




    def Handle_Buttons(self):
        ##login
        self.login_button.clicked.connect(self.login_button_action)
        ##main
        self._home_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self._payroll_button.clicked.connect(self.show_payroll_home)
        self._payroll_button.clicked.connect(lambda:self.tabWidget.setCurrentIndex(2))
        self._payslip_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(5))
        self._quit_button.clicked.connect(self._quit_button_action)
        self._settings_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(6))
        self._settings_button.clicked.connect(self.show_settings)
        ##payroll_home
        self.payroll_home_new.clicked.connect(self.payroll_home_new_action)
        self.payroll_home_edit.clicked.connect(self.payroll_home_edit_action)
        self.payroll_home_view.clicked.connect(self.payroll_home_view_action)
        ##payroll_view
        self.payroll_view_quit.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        ##payroll_ae
        self.payroll_ae_add_person.clicked.connect(self.payroll_ae_add_person_action)
        self.payroll_ae_quit.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        ##settings
        self.settings_edit_account.clicked.connect(lambda: self.settings_account_table_edit(self.settings_table_widget_accounts))
        self.settings_add_account.clicked.connect(lambda: self.settings_account_table_add(self.settings_table_widget_accounts))
        self.settings_delete_account.clicked.connect(lambda: self.settings_account_table_delete(self.settings_table_widget_accounts))
        self.settings_edit_signatory.clicked.connect(lambda: self.settings_signatory_table_edit(self.settings_table_widget_signatory))


########################MENU BUTTONS##################################

    def _quit_button_action(self):
        self.login_warning.setText(' ')
        self.tabWidget.setCurrentIndex(0)
        self._container.setVisible(False)

#--------------------------------------------------------------------#



######################## Login Tab####################################
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

#--------------------------------------------------------------------#


#######################PAYROLL_HOME TAB ##############################

    def payroll_home_new_action(self):
        ad = Add_Payroll_Dialogue(self)
        ad.show()
        ad.Show_Payroll('add')
        #self.tabWidget.setCurrentIndex(4)


    def payroll_home_edit_action(self):
        self.tabWidget.setCurrentIndex(4)


    def payroll_home_view_action(self):
        self.tabWidget.setCurrentIndex(3)


    def show_payroll_home(self):
        global payroll_home_list_dict
        global payroll_home_list_widget
        payroll_home_list_widget.clear()
        payroll_home_list_dict = {}

        engine = sqc.Database().engine
        conn = engine.connect()
        payroll_bundle = sqc.Database().payroll_bundle
        s = payroll_bundle.select()
        s_value = conn.execute(s)
        for val in s_value:
            payroll_home_list_dict.update({
                val[0] : '{}|{}'.format(val[1],val[2])
            })
        for key,value in payroll_home_list_dict.items():
            item = QtWidgets.QListWidgetItem(value)
            payroll_home_list_widget.addItem(item)

#--------------------------------------------------------------------#



#######################PAYROLL_AE TAB ###############################

    def payroll_ae_add_person_action(self):
        dialog = Add_Employee_Dialogue(self)
        dialog.show()

#--------------------------------------------------------------------#




####################### SETTINGS TAB ###############################

    def show_settings(self):
        self.settings_table_widget_accounts.setRowCount(0)
        self.settings_table_widget_salary_grade.setRowCount(0)
        self.settings_table_widget_signatory.setRowCount(0)

        engine = sqc.Database().engine
        payroll_admin = sqc.Database().payroll_admin
        payroll_salarygrade = sqc.Database().payroll_salarygrade
        payroll_signatory = sqc.Database().payroll_signatory

        conn = engine.connect()
        s = payroll_admin.select()
        s_value = conn.execute(s)
        table = self.settings_table_widget_accounts
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))
            table.setItem(row_position, 3, QTableWidgetItem(str(val[3])))

        s = payroll_salarygrade.select()
        s_value = conn.execute(s)
        table=self.settings_table_widget_salary_grade
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))

        s = payroll_signatory.select()
        s_value = conn.execute(s)
        table=self.settings_table_widget_signatory
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))


    def settings_account_table_edit(self,table):
        try:
            r = table.currentRow()
            id = table.item(r,0).text()
            username = table.item(r,1).text()
            password = table.item(r,2).text()
            previlage = table.item(r,3).text()

            ad = Accounts_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id,username,password,operationType='edit')
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Rows Selected')
            msg.setWindowTitle("Error")
            msg.exec_()

    def settings_account_table_add(self,table):
        try:
            ad = Accounts_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id,'','',operationType='add')
        except:
            pass

    def settings_account_table_delete(self,table):
        r = table.currentRow()
        id = table.item(r, 0).text()
        engine = sqc.Database().engine
        conn = engine.connect()
        payroll_admin = sqc.Database().payroll_admin
        s = payroll_admin.delete().where(payroll_admin.c.userid == id)
        conn.execute(s)
        self.show_settings()

    def settings_signatory_table_edit(self,table):
        try:
            r = table.currentRow()
            id = table.item(r,0).text()
            name = table.item(r,1).text()
            designation = table.item(r,2).text()
            ad = Signatories_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id,name,designation)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Rows Selected')
            msg.setWindowTitle("Error")
            msg.exec_()
#--------------------------------------------------------------------#



###########################################DIALOGS#####################################

class Add_Payroll_Dialogue(QDialog,add_payroll_ui):
    operationType = ''
    def __init__(self,parent=None):
        super(Add_Payroll_Dialogue,self).__init__(parent)
        self.setupUi(self)
        self.Handle_UI_Changes()

    def Handle_UI_Changes(self):
        self.logo.setEnabled(False)

        month = convertMonth(int(datetime.datetime.now().month))

        day = int(datetime.datetime.now().day)
        year = int(datetime.datetime.now().year)

        index = self.from_year.findText('{}'.format(year),QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.from_year.setCurrentIndex(index)
        index = self.from_month.findText('{}'.format(month),QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.from_month.setCurrentIndex(index)
        index = self.from_day.findText('{}'.format(day),QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.from_day.setCurrentIndex(index)
        index = self.to_year.findText('{}'.format(year),QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.to_year.setCurrentIndex(index)
        index = self.to_month.findText('{}'.format(month),QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.to_month.setCurrentIndex(index)
        index = self.to_day.findText('{}'.format(day),QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.to_day.setCurrentIndex(index)



    def Show_Payroll(self,operationType):
        self.operationType = operationType
        self.buttonBox.accepted.connect(self.ok_button)


    def ok_button(self):
        if self.operationType == 'add':
            engine = sqc.Database().engine
            payroll_bundle = sqc.Database().payroll_bundle
            conn = engine.connect()

            try:
                py_date_from = '{}-{}-{}'.format(self.from_month.currentText(),self.from_day.currentText(),self.from_year.currentText())
                py_date_to = '{}-{}-{}'.format(self.to_month.currentText(), self.to_day.currentText(),self.to_year.currentText())
                s = payroll_bundle.insert().values(
                    payroll_date_from=py_date_from,
                    payroll_date_to=py_date_to
                )
                conn.execute(s)

            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Error in data input')
                msg.setWindowTitle("Error")
                msg.exec_()
        self.show_payroll_home()


    def show_payroll_home(self):
        global payroll_home_list_dict
        global payroll_home_list_widget
        payroll_home_list_widget.clear()
        payroll_home_list_dict = {}

        engine = sqc.Database().engine
        conn = engine.connect()
        payroll_bundle = sqc.Database().payroll_bundle
        s = payroll_bundle.select()
        s_value = conn.execute(s)
        for val in s_value:
            payroll_home_list_dict.update({
                val[0] : '{}|{}'.format(val[1],val[2])
            })
        for key,value in payroll_home_list_dict.items():
            item = QtWidgets.QListWidgetItem(value)
            payroll_home_list_widget.addItem(item)








class Add_Employee_Dialogue(QDialog,add_employee_ui):
    def __init__(self,parent=None):
        super(Add_Employee_Dialogue,self).__init__(parent)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Button_Changes()

    def Handle_UI_Changes(self):
        pass
    def Handle_Button_Changes(self):
        pass






######################################Settings Dialog##########################################

class Accounts_Dialogue(QDialog,accounts_ui):
    edit_id = 0
    operationType = ''
    def __init__(self,parent=None):
        super(Accounts_Dialogue,self).__init__(parent)
        self.setupUi(self)

    def ShowDialogue(self,id,username,password,dependencies='',operationType = ''):
        self.username.setText(username)
        self.password.setText(password)
        self.edit_id = id
        self.operationType = operationType
        self.buttonBox.accepted.connect(self.ok_button)

    def ok_button(self):
        engine = sqc.Database().engine
        payroll_admin = sqc.Database().payroll_admin
        conn = engine.connect()

        if self.operationType == 'edit':
            s = payroll_admin.update().where(payroll_admin.c.userid == self.edit_id).\
                values(username = self.username.text(),
                       password = self.password.text(),
                       previlage = self.previlage_combo.currentText())
            conn.execute(s)
            self.show_settings()

        elif self.operationType == 'add':
            s = payroll_admin.insert().values(
                username=self.username.text(),
                password=self.password.text(),
                previlage=self.previlage_combo.currentText()
            )
            conn.execute(s)
            self.show_settings()

    def show_settings(self):
        global settings_table_widget_accounts
        settings_table_widget_accounts.setRowCount(0)
        engine = sqc.Database().engine
        payroll_admin = sqc.Database().payroll_admin
        conn = engine.connect()
        s = payroll_admin.select()
        s_value = conn.execute(s)
        table = settings_table_widget_accounts
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))
            table.setItem(row_position, 3, QTableWidgetItem(str(val[3])))


class Signatories_Dialogue(QDialog,signatories_ui):
    edit_id = 0
    def __init__(self,parent=None):
        super(Signatories_Dialogue,self).__init__(parent)
        self.setupUi(self)

    def ShowDialogue(self,id,name,designation):
        self.name.setText(name)
        self.designation.setText(designation)
        self.edit_id = id
        self.buttonBox.accepted.connect(self.ok_button)

    def ok_button(self):
        engine = sqc.Database().engine
        payroll_signatory = sqc.Database().payroll_signatory
        conn = engine.connect()
        s = payroll_signatory.update().where(payroll_signatory.c.signatoryid == self.edit_id).\
            values(name = self.name.text(),
                   designation = self.designation.text())
        conn.execute(s)
        self.show_settings()

    def show_settings(self):
        global settings_table_widget_signatory
        settings_table_widget_signatory.setRowCount(0)
        engine = sqc.Database().engine
        payroll_signatory = sqc.Database().payroll_signatory
        conn = engine.connect()
        s = payroll_signatory.select()
        s_value = conn.execute(s)
        table = settings_table_widget_signatory
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))




def convertMonth(month):
    tempdict = {
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 : 'November',
        12 : 'December'
    }
    return tempdict[month]



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

