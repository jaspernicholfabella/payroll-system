from sqlalchemy import create_engine
from sqlalchemy import Table, Column,VARCHAR,INTEGER,Float,String, MetaData,ForeignKey,Date,Text,DECIMAL
from sqlalchemy.sql import exists
import os
class Database():
    engine = create_engine('sqlite:///{}/db/sor_gov_hr.db'.format(os.getcwd()))
    meta = MetaData()

    employee = Table('employee',meta,
                    Column('employee_id',INTEGER,primary_key=True),
                    Column('lname',VARCHAR(30)),
                    Column('fname',VARCHAR(30)),
                    #Column('midname',VARCHAR(30)),
                     Column('midinit',VARCHAR(5)),
                    # Column('birthdate',Date),
                    # Column('birthplace',VARCHAR(50)),
                    # Column('gender',VARCHAR(1)),
                    # Column('civilstatus',VARCHAR(20)),
                    # Column('height',VARCHAR(6)),
                    # Column('weight',VARCHAR(6)),
                    # Column('bloodtype',VARCHAR(2)),
                    # Column('gsisno',VARCHAR(20)),
                    # Column('pagibigno',VARCHAR(20)),
                    # Column('philhealthno',VARCHAR(20)),
                    # Column('sssno',VARCHAR(20)),
                    # Column('tinno',VARCHAR(20)),
                    # Column('agencyemployeeno',VARCHAR(20)),
                    # Column('citizenship',VARCHAR(15)),
                    # Column('residentialaddr1',Text),
                    # Column('residentialaddr2',Text),
                    # Column('residentialaddr3',Text),
                    # Column('residentialaddr4',Text),
                    # Column('reszipcode',VARCHAR(5)),
                    # Column('permanentaddr1',Text),
                    # Column('permanentaddr2',Text),
                    # Column('permanentaddr3',Text),
                    # Column('permanentaddr4',Text),
                    # Column('permzipcode',VARCHAR(5)),
                    # Column('telno',VARCHAR(15)),
                    # Column('mobileno',VARCHAR(15)),
                    # Column('emailaddr',VARCHAR(30)),
                    # Column('spouselname',VARCHAR(30)),
                    # Column('spousefname',VARCHAR(30)),
                    # Column('spousemname',VARCHAR(30)),
                    # Column('sp_occupation',Text),
                    # Column('sp_employer',Text),
                    # Column('sp_empraddr',Text),
                    # Column('sp_emprtelno',VARCHAR(15)),
                    # Column('fatherlname',VARCHAR(30)),
                    # Column('fatherfname',VARCHAR(30)),
                    # Column('fathermname',VARCHAR(30)),
                    # Column('motherlname',VARCHAR(30)),
                    # Column('motherfname',VARCHAR(30)),
                    # Column('mothermname',VARCHAR(30)),
                    # mysql_engine='InnoDB',
                    # mysql_charset='utf8mb4',
                    # mysql_key_block_size="1024",
                     )


    salarygrade = Table('salarygrade',meta,
                        Column('salaryid', INTEGER, primary_key=True),
                        Column('salarytitle', VARCHAR(8)),
                        Column('amount',Float))

    payroll_designation = Table('payroll_designation',meta,
                        Column('designationid', INTEGER, primary_key=True),
                        Column('designationtitle', String),
                        Column('salarygrade',String))

    payroll_admin = Table('payroll_admin',meta,
                          Column('userid',INTEGER,primary_key=True),
                          Column('username',VARCHAR(50)),
                          Column('password',VARCHAR(50)),
                          Column('previlage',VARCHAR(50)),
                          Column('employee_id',INTEGER))

    payroll_signatory = Table('payroll_signatory',meta,
                              Column('signatoryid',INTEGER,primary_key=True),
                              Column('name',String),
                              Column('designation',String))

    payroll_bundle = Table('payroll_bundle',meta,
                           Column('payrollid',INTEGER,primary_key=True),
                           Column('payroll_date_from',String),
                           Column('payroll_date_to',String),
                           Column('payroll_name',String))
                           #Column('payroll_offices',String))


    payroll_record = Table('payroll_record',meta,
                           Column('recordid',INTEGER,primary_key=True),
                           Column('payrollid', INTEGER),
                           Column('employee_id', INTEGER),
                           Column('name',String),
                           Column('designation',String),
                           Column('monthly_rate',Float),
                           Column('amount_accrued',Float),
                           Column('pera',Float),
                           Column('amount',Float),
                           Column('tax',Float),
                           Column('gsis_educ',Float),
                           Column('pagibig_personal',Float),
                           Column('pagibig_gov',Float),
                           Column('pagibig_mpl',Float),
                           Column('pagibig_calam_loan',Float),
                           Column('pagibig_housing_loan',Float),
                           Column('philhealth_personal',Float),
                           Column('philhealth_gov',Float),
                           Column('ruralbank_pilar',Float),
                           Column('gempco_reg',Float),
                           Column('gempco_educ',Float),
                           Column('soprecco_reg',Float),
                           Column('soprecco_educ',Float),
                           Column('soprecco_share',Float),
                           Column('amout_due',Float))


    meta.create_all(engine)

    conn = engine.connect()
    s = payroll_signatory.select()
    s_value = conn.execute(s)
    x = 0
    for val in s_value:
        x += 1


    signatories = {
        'FRANCIS JOSEPH G. ESCUDERO':'Governor',
        'CRISTE L. DAGÑALAN':'AO IV (HRMO II)',
        'ARTHUR M. BALMADRID':'PGDH/PHRMO',
        'MERCEDES J. ATIVO':'Provincial Accountant',
        'BELINDA J. GACOSTA':'Acting Provincial Treasurer'
    }


    if x < 4:
        for key,item in signatories.items():
            print('{} : {}'.format(key,item))
            ins = payroll_signatory.insert().values(name = key,designation = item)



    s = payroll_admin.select()
    s_value = conn.execute(s)
    z = 0
    for val in s_value:
        z += 1

    if z == 0:
        ins = payroll_admin.insert().values(username = 'admin',
                                            password = 'admin',
                                            previlage = 'admin',
                                            employee_id = 0)
        result = conn.execute(ins)