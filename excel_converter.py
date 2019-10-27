import sys
import os
import sqlconn as sqc
from sqlalchemy import desc, asc
import win32com.client as wstp
import xlwings.constants

def open_excel(payrollid):
    payroll_employee_dict = {}
    engine = sqc.Database().engine
    conn = engine.connect()
    payroll_bundle = sqc.Database().payroll_bundle
    s = payroll_bundle.select().where(payroll_bundle.c.payrollid == payrollid)
    s_value = conn.execute(s)
    for val in s_value:
        payroll_name = val[3]

    mydirectory = '{}\{}'.format(os.getcwd(),'payroll_readonly.xls')
    excel = wstp.DispatchEx('Excel.Application')
    book = excel.Workbooks.Open(str(mydirectory),ReadOnly = True)
    sheet = book.Worksheets(1)
    excel.Visible = True
    payroll_title = payroll_name.split('#')[0].strip()
    payroll_title = str(payroll_title[1:])
    sheet.Range("A4").Value = payroll_title

    conn = engine.connect()
    employee = sqc.Database().employee
    s = employee.select()
    s_value = conn.execute(s)
    for val in s_value:
        payroll_employee_dict.update({val[0] : '{} {} {}'.format(val[2],val[3],val[1])})

    conn = engine.connect()
    payroll_record = sqc.Database().payroll_record
    s = payroll_record.select().where(payroll_record.c.payrollid == payrollid)
    s_value = conn.execute(s)
    for val in s_value:
        range_insert = sheet.Range("A11:X11")
        range_insert.EntireRow.Insert()

    conn = engine.connect()
    payroll_record = sqc.Database().payroll_record
    s = payroll_record.select().where(payroll_record.c.payrollid == payrollid).order_by(desc(payroll_record.c.monthly_rate))
    s_value = conn.execute(s)
    i = 1
    row = 10
    for val in s_value:
        sheet.Cells(row,1).Value = i
        sheet.Cells(row,1).Borders.LineStyle= xlwings.constants.LineStyle.xlContinuous
        sheet.Cells(row,2).Value = (payroll_employee_dict[int(val[2])])
        sheet.Cells(row,2).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        sheet.Cells(row,3).Value = val[4]
        sheet.Cells(row,3).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        sheet.Cells(row,4).Value = val[5]
        sheet.Cells(row,4).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        sheet.Cells(row,5).Value = val[6]
        sheet.Cells(row,5).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        sheet.Cells(row,6).Value = val[7]
        sheet.Cells(row,6).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        sheet.Cells(row,7).Value = val[6] + val[7]
        sheet.Cells(row,7).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        total = 0.0
        for x in range(9,24):
            if val[x] < 1:
                #sheet.Cells(row,x-1).Value = '-'
                sheet.Cells(row, x - 1).Value = val[x]
            else:
                sheet.Cells(row,x-1).Value = val[x]
            sheet.Cells(row,x-1).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
            total += val[x]

        sheet.Cells(row,23).Value = (val[6] + val[7]) - total
        sheet.Cells(row,23).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        sheet.Cells(row,24).Value = i
        sheet.Cells(row,24).Borders.LineStyle =  xlwings.constants.LineStyle.xlContinuous
        row += 1
        i += 1
    templist = ['D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W']
    print(row)
    sheet.Cells(row, 1).Borders.LineStyle = xlwings.constants.LineStyle.xlContinuous
    sheet.Cells(row, 2).Borders.LineStyle = xlwings.constants.LineStyle.xlContinuous
    sheet.Cells(row, 3).Value = 'TOTAL'
    sheet.Cells(row, 3).Borders.LineStyle = xlwings.constants.LineStyle.xlContinuous
    z = 4
    for letter in templist:
        sheet.Cells(row, z).Formula = "=SUM({}10:{}{})".format(letter,letter,row - 1)
        sheet.Cells(row, z).Borders.LineStyle = xlwings.constants.LineStyle.xlContinuous
        z+=1
    sheet.Cells(row, 24).Borders.LineStyle = xlwings.constants.LineStyle.xlContinuous
    




def find_cell(scsht,tofind,srow = 1,scol = 1,lrow = 1,lcol = 1,search_order = 'by_row', search_sheet = 'advance', lookin = 'formulas'):
    """
    :param scsht: source sheet object #cannot be None
    :param tofind: string #cannot be None
    :param srow: start row, integer #default 1
    :param scol: start column, integer #default 1
    :param lrow: last row, integer, #default 1
    :param lcol: last column, integer #default 1
    :param search_order: 'by_row' or 'by_col', string #default 'by_row'
    :param search_sheet: 'advance' or 'basic' if basic no lrow or lcol needed. #default is advance
    :param lookin: 'formulas','values' or 'comments' #default formulas
    :return: dict['row'] and dict['col']
    """
    search_order_dict = {'by_row' : xlwings.constants.SearchOrder.xlByRows,'by_col' : xlwings.constants.SearchOrder.xlByColumns}
    lookin_dict = {'values':xlwings.constants.FindLookIn.xlValues,'formulas':xlwings.constants.FindLookIn.xlFormulas,'comments':xlwings.constants.FindLookIn.xlComments}
    if search_sheet == 'advance':
        cell = scsht.Range(scsht.Cells(srow, scol), scsht.Cells(lrow, lcol)).Find(What=tofind.strip(), LookAt=xlwings.constants.LookAt.xlWhole,LookIn=lookin_dict[lookin],SearchOrder=xlwings.constants.SearchOrder.xlByRows, MatchCase=False)
        if cell is None:
            cell = scsht.Range(scsht.Cells(srow, scol), scsht.Cells(lrow, lcol)).Find(What=tofind.strip(), LookAt=xlwings.constants.LookAt.xlPart,LookIn=lookin_dict[lookin],SearchOrder=search_order_dict[search_order], MatchCase=False)
        print('{} at , row = {}, col = {}'.format(tofind, cell.Row, cell.Column))
    elif search_sheet == 'basic':
        cell = scsht.Cells.Find(What="*", After=scsht.Cells(1, 1),SearchOrder=search_order_dict[search_order],SearchDirection=xlwings.constants.SearchDirection.xlPrevious)
    cellpos = {'row' : cell.Row,'col' : cell.Column}
    return cellpos
