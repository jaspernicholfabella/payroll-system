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
global tabWidget
global settings_table_widget_accounts
global settings_table_widget_salary_grade
global settings_table_widget_salary_designation
global settings_table_widget_signatory
global payroll_home_list_dict
global payroll_home_list_widget
global payroll_ae_title
global payroll_ae_secret_id
global payroll_ae_table_widget
global payroll_employee_dict
global salary_grade_dict



main_ui, _ = loadUiType('Payroll_System.ui')
add_payroll_ui, _ = loadUiType('Add_Payroll.ui')
add_employee_ui, _ = loadUiType('Add_Employee.ui')
accounts_ui, _ = loadUiType('Accounts.ui')
salary_grade_ui, _ = loadUiType('SalaryGrade.ui')
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
        # self.login_title.setText('PHRMO Payroll Information System')
        # self.home_title.setText('PHRMO Payroll Information System')
        # self.home_text.setText('This System is created as a Capstone Project from Sorsogon State College 2019 ©')
        # self.payroll_home_title.setText('Payroll Record')
        # self.settings_account_title.setText('Accounts')
        # self.settings_salary_grade_title.setText('Salary Grade')
        # self.settings_salary_grade_designation.setText('Designation')
        # self.settings_signatory_title.setText('Signatory')
        # self.payslip_title.setText('Employee Payslip Records')
        pass


    def Handle_UI_Changes(self):
        ##globals
        global tabWidget
        global settings_table_widget_accounts
        global settings_table_widget_salary_grade
        global settings_table_widget_salary_designation
        global settings_table_widget_signatory
        global payroll_home_list_widget
        global payroll_ae_title
        global payroll_ae_secret_id
        global payroll_ae_table_widget
        ##main
        tabWidget = self.tabWidget
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
        payroll_ae_title = self.payroll_ae_title
        payroll_ae_secret_id = self.payroll_ae_secret_id
        payroll_ae_table_widget = self.payroll_ae_table_widget
        #payroll_ae_secret_id.setVisible(False)
        self.payroll_ae_table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.payroll_ae_employee_dict_update()
        ##payslip
        self.payslip_logo_1.setEnabled(False)
        self.payslip_logo_2.setEnabled(False)
        self.payslip_tab_widget.tabBar().setVisible(False)
        self.payslip_tab_widget.setCurrentIndex(0)
        ##settings
        self.show_settings()
        self.settings_table_widget_accounts.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_table_widget_salary_grade.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_table_widget_salary_designation.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_table_widget_signatory.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_table_widget_accounts.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.settings_table_widget_salary_grade.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.settings_table_widget_salary_designation.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.settings_table_widget_signatory.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        #self.settings_table_widget_accounts.resizeColumnsToContents()
        #self.settings_table_widget_salary_grade.resizeColumnsToContents()
        # self.settings_table_widget_salary_designation.resizeColumnsToContents()
        self.settings_table_widget_signatory.resizeColumnsToContents()
        self.settings_table_widget_accounts.setColumnHidden(0,True)
        self.settings_table_widget_salary_grade.setColumnHidden(0,True)
        self.settings_table_widget_salary_designation.setColumnHidden(0, True)
        self.settings_table_widget_signatory.setColumnHidden(0,True)
        settings_table_widget_accounts = self.settings_table_widget_accounts
        settings_table_widget_salary_grade = self.settings_table_widget_salary_grade
        settings_table_widget_salary_designation = self.settings_table_widget_salary_designation
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
        self.payroll_home_delete.clicked.connect(self.payroll_home_delete_action)
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
        self.settings_edit_salary_grade.clicked.connect(lambda: self.settings_salary_grade_table_edit(self.settings_table_widget_salary_grade))
        self.settings_add_salary_grade.clicked.connect(lambda: self.settings_salary_grade_table_add(self.settings_table_widget_salary_grade))
        self.settings_delete_salary_grade.clicked.connect(lambda: self.settings_salary_grade_table_delete(self.settings_table_widget_salary_grade))

        self.settings_edit_salary_designation.clicked.connect(lambda: self.settings_salary_designation_table_edit(self.settings_table_widget_salary_designation))
        self.settings_add_salary_designation.clicked.connect(lambda: self.settings_salary_designation_table_add(self.settings_table_widget_salary_designation))
        self.settings_delete_salary_designation.clicked.connect(lambda: self.settings_salary_designation_table_delete(self.settings_table_widget_salary_designation))

        self.settings_edit_signatory.clicked.connect(lambda: self.settings_signatory_table_edit(self.settings_table_widget_signatory))


##MENU BUTTONS
#____________________________________________________________________________________________________#
    def _quit_button_action(self):
        self.login_warning.setText(' ')
        self.tabWidget.setCurrentIndex(0)
        self._container.setVisible(False)


##LOGIN TAB
#____________________________________________________________________________________________________#
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


##PAYROLL HOME TAB
#____________________________________________________________________________________________________#

    def payroll_home_new_action(self):
        ad = Add_Payroll_Dialogue(self)
        ad.show()
        ad.Show_Payroll('add')
        #self.tabWidget.setCurrentIndex(4)


    def payroll_home_edit_action(self):
        global payroll_home_list_widget
        global payroll_home_list_dict
        global payroll_ae_secret_id
        try:
            id = payroll_home_list_dict[payroll_home_list_widget.currentItem().text()]
            self.tabWidget.setCurrentIndex(4)
            payroll_ae_secret_id.setText(str(id))
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Data Selected')
            msg.setWindowTitle("Error")
            msg.exec_()


    def payroll_home_delete_action(self):
        global payroll_home_list_dict
        global payroll_home_list_widget
        try:
            print(payroll_home_list_widget.currentItem().text())
            id = payroll_home_list_dict[payroll_home_list_widget.currentItem().text()]
            engine = sqc.Database().engine
            payroll_bundle = sqc.Database().payroll_bundle
            conn = engine.connect()
            q = payroll_bundle.delete().where(payroll_bundle.c.payrollid == int(id))
            conn.execute(q)
            self.show_payroll_home()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Data Selected')
            msg.setWindowTitle("Error")
            msg.exec_()





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
                val[3] : val[0]
            })
        for key,value in payroll_home_list_dict.items():
            item = QtWidgets.QListWidgetItem(key)
            payroll_home_list_widget.addItem(item)

##PAYROLL AE TAB
#___________________________________________________________________________________________________#

    def payroll_ae_add_person_action(self):
        dialog = Add_Employee_Dialogue(self)
        dialog.show()


    def payroll_ae_employee_dict_update(self):
        global payroll_employee_dict
        payroll_employee_dict = {}
        engine = sqc.Database().engine
        employee = sqc.Database().employee
        conn = engine.connect()
        s = employee.select()
        s_value = conn.execute(s)
        for val in s_value:
            payroll_employee_dict.update({
                '{}, {} {}'.format(val[1],val[2],val[3]) : val[0]
            })

##SETTINGS TAB
#___________________________________________________________________________________________________#
    def show_settings(self):
        self.settings_table_widget_accounts.setRowCount(0)
        self.settings_table_widget_salary_grade.setRowCount(0)
        self.settings_table_widget_salary_designation.setRowCount(0)
        self.settings_table_widget_signatory.setRowCount(0)

        engine = sqc.Database().engine
        payroll_admin = sqc.Database().payroll_admin
        salarygrade = sqc.Database().salarygrade
        designation = sqc.Database().payroll_designation
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

        s = salarygrade.select()
        s_value = conn.execute(s)
        table=self.settings_table_widget_salary_grade
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))

        s = designation.select()
        s_value = conn.execute(s)
        table=self.settings_table_widget_salary_designation
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





    def settings_salary_grade_table_edit(self,table):
        try:
            r = table.currentRow()
            id = table.item(r,0).text()
            tempsg = table.item(r,1).text()
            amount = table.item(r,2).text()

            salarygrade = str(tempsg).split('-')[1].strip()
            step = str(tempsg).split('-')[2].strip()

            ad = Salary_Grade_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id,salarygrade,step,amount,operationType='edit')

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Rows Selected')
            msg.setWindowTitle("Error")
            msg.exec_()

    def settings_salary_grade_table_add(self,table):
        try:
            ad = Salary_Grade_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id,'','','',operationType='add')
        except:
            pass

    def settings_salary_grade_table_delete(self,table):
        r = table.currentRow()
        id = table.item(r, 0).text()
        engine = sqc.Database().engine
        conn = engine.connect()
        salarygrade = sqc.Database().salarygrade
        s = salarygrade.delete().where(salarygrade.c.salaryid == id)
        conn.execute(s)
        self.show_settings()




    def settings_salary_designation_table_edit(self,table):
        try:
            r = table.currentRow()
            id = table.item(r,0).text()
            designation = table.item(r,1).text()
            salarygrade = table.item(r,2).text()
            ad = Designation_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id,designation,salarygrade,operationType='edit')

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Rows Selected')
            msg.setWindowTitle("Error")
            msg.exec_()

    def settings_salary_designation_table_add(self,table):
        try:
            ad = Designation_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id,'','',operationType='add')
        except:
            pass

    def settings_salary_designation_table_delete(self,table):
        r = table.currentRow()
        id = table.item(r, 0).text()
        engine = sqc.Database().engine
        conn = engine.connect()
        designation = sqc.Database().payroll_designation
        s = designation.delete().where(designation.c.designationid == id)
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


#___________________________________________________DIALOGUE_________________________________________#

#____________________________________________________________________________________________________#


##ADD PAYROLL
#____________________________________________________________________________________________________#

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
                py_name = ''

                if self.from_month.currentText() == self.to_month.currentText():
                    py_name = '✎FOR THE PERIOD {} {}-{}, {} #[{}]'.format(self.from_month.currentText(),
                                                                     self.from_day.currentText(),
                                                                     self.to_day.currentText(),
                                                                     self.from_year.currentText(),
                                                                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    if self.from_year.currentText() == self.to_year.currentText():
                        py_name = '✎FOR THE PERIOD {} {} - {} {}, {} #[{}]'.format(self.from_month.currentText(),
                                                                        self.from_day.currentText(),
                                                                        self.to_month.currentText(),
                                                                        self.to_day.currentText(),
                                                                        self.from_year.currentText(),
                                                                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        py_name = '✎FOR THE PERIOD {} {}, {} - {} {}, {} #[{}]'.format(self.from_month.currentText(),
                                                                        self.from_day.currentText(),
                                                                        self.from_year.currentText(),
                                                                        self.to_month.currentText(),
                                                                        self.to_day.currentText(),
                                                                        self.to_year.currentText(),
                                                                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                s = payroll_bundle.insert().values(
                    payroll_date_from=py_date_from,
                    payroll_date_to=py_date_to,
                    payroll_name = py_name
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
        self.go_payroll_ae_add()


    def go_payroll_ae_add(self):
        global tabWidget
        global payroll_home_list_dict
        global payroll_ae_secret_id
        global payroll_ae_title
        id = 0
        temp_key = ''
        for key, value in payroll_home_list_dict.items():
            id = value
            temp_key = key
        temp = temp_key.split('#')[0].strip()
        tabWidget.setCurrentIndex(4)
        payroll_ae_title.setText(temp)
        payroll_ae_secret_id.setText(str(id))



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
                val[3] : val[0]
            })
        for key,value in payroll_home_list_dict.items():
            item = QtWidgets.QListWidgetItem(key)
            payroll_home_list_widget.addItem(item)

##ADD_EMPLOYEE
#________________________________________________________________________________________________________________________________#
class Add_Employee_Dialogue(QDialog,add_employee_ui):

    def __init__(self,parent=None):
        super(Add_Employee_Dialogue,self).__init__(parent)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Button_Changes()

    def Handle_UI_Changes(self):
        global payroll_employee_dict
        x = 0
        for key,value in payroll_employee_dict.items():
            self._add_employee_name_combo.addItem(key)
            x+=1

    def Handle_Button_Changes(self):
        pass










#______________________________________________________________________________________________________#





##SETTINGS
#_____________________________________________________________________________________________________#
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


class Salary_Grade_Dialogue(QDialog,salary_grade_ui):
    edit_id = 0
    operationType = ''
    def __init__(self,parent=None):
        super(Salary_Grade_Dialogue,self).__init__(parent)
        self.setupUi(self)

    def ShowDialogue(self,id,salarygrade,step,salary,operationType = ''):
        self.salarygrade.setText(salarygrade)
        self.step.setText(step)
        self.salary.setText(salary)
        self.edit_id = id
        self.operationType = operationType
        self.buttonBox.accepted.connect(self.ok_button)


    def ok_button(self):
        try:
            sg = int(self.salarygrade.text())
            step = int(self.step.text())
            engine = sqc.Database().engine
            salarygrade = sqc.Database().salarygrade
            conn = engine.connect()
            salarytitle = 'sg-{}-{}'.format(sg,step)
            if self.operationType == 'edit':
                s = salarygrade.update().where(salarygrade.c.salaryid == self.edit_id).\
                    values(salarytitle = salarytitle,
                           amount = float(self.salary.text()))
                conn.execute(s)
                self.show_settings()

            elif self.operationType == 'add':
                s = salarygrade.insert().values(
                    salarytitle = salarytitle,
                    amount = float(self.salary.text())
                )
                conn.execute(s)
            self.show_settings()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Data Should be numeric.')
            msg.setWindowTitle("Error")
            msg.exec_()


    def show_settings(self):
        global settings_table_widget_salary_grade
        settings_table_widget_salary_grade.setRowCount(0)
        engine = sqc.Database().engine
        salarygrade = sqc.Database().salarygrade
        conn = engine.connect()
        s = salarygrade.select()
        s_value = conn.execute(s)
        table = settings_table_widget_salary_grade
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))




class Designation_Dialogue(QDialog,designation_ui):
    edit_id = 0
    operationType = ''
    def __init__(self,parent=None):
        super(Designation_Dialogue,self).__init__(parent)
        self.setupUi(self)
        self.Salarygrade_Values()


    def Salarygrade_Values(self):
        global salary_grade_dict
        salary_grade_dict = {}

        engine = sqc.Database().engine
        salarygrade = sqc.Database().salarygrade
        conn = engine.connect()
        s = salarygrade.select()
        s_value = conn.execute(s)

        for val in s_value:
            salary_grade_dict.update({val[1]:val[2]})

        for key,item in salary_grade_dict.items():
            self.salarygrade_combo.addItem(key)


    def ShowDialogue(self,id,designation,salary_grade,operationType = ''):

        index = self.salarygrade_combo.findText(salary_grade)
        if index >= 0:
            self.salarygrade_combo.setCurrentIndex(index)

        self.designation.setText(designation)
        self.edit_id = id
        self.operationType = operationType
        self.buttonBox.accepted.connect(self.ok_button)


    def ok_button(self):
        engine = sqc.Database().engine
        payroll_designation = sqc.Database().payroll_designation
        conn = engine.connect()
        if self.operationType == 'edit':
            s = payroll_designation.update().where(payroll_designation.c.designationid == self.edit_id).\
                values(designationtitle = self.designation.text(),
                       salarygrade = self.salarygrade_combo.currentText())
            conn.execute(s)
            self.show_settings()

        elif self.operationType == 'add':
            s = payroll_designation.insert().values(
                designationtitle=self.designation.text(),
                salarygrade=self.salarygrade_combo.currentText()
            )
            conn.execute(s)
        self.show_settings()



    def show_settings(self):
        global settings_table_widget_salary_designation
        settings_table_widget_salary_designation.setRowCount(0)
        engine = sqc.Database().engine
        designation = sqc.Database().payroll_designation
        conn = engine.connect()
        s = designation.select()
        s_value = conn.execute(s)
        table = settings_table_widget_salary_designation
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))





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

