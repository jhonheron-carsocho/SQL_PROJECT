from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
import pandas as pd
from kivymd_extensions.akivymd import *
import mysql
from xlsxwriter import worksheet
from xlsxwriter import workbook
from xlsxwriter.workbook import Workbook
from datetime import date
from libs.baseclass import db_conn
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.properties import NumericProperty
import datetime


Builder.load_file('./libs/kv/lobby.kv')

class Lobby(Screen):
    visitors = NumericProperty(0)

    def on_enter(self, *args):
        conn = db_conn.data_base()
        cur = conn.cursor()

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 1 DAY)""")
        get = cur.fetchall()
        self.visitors = get[0][0]

class RightSide(BoxLayout):
    def export_data(self):
        path = './Exports'

        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
        
            # Create a new directory because it does not exist 
            os.makedirs(path)

        dates = []
        conn = db_conn.data_base()
        cur = conn.cursor()
        cur.execute("""SELECT name, age, address, number, DATE_FORMAT(time_in, "%H:%i"), DATE_FORMAT(time_out, "%H:%i"), DATE_FORMAT(time_in, "%M %D %Y")
                    from customers""")
        res = cur.fetchall()

        for i in res:
            if i[6] not in dates:
                dates.append(i[6])

        for d in dates:
            row_n = 1
            title = './Exports/TRACE ' + str(d) + '.xlsx'
            workbook = Workbook(title)
            worksheet = workbook.add_worksheet()
            
            # writes column names to spreadsheet
            worksheet.write('A1', 'Name')
            worksheet.write('B1', 'Age')
            worksheet.write('C1', 'Address')
            worksheet.write('D1', 'Contact Number')
            worksheet.write('E1', 'Time In')
            worksheet.write('F1', 'Time Out')
            worksheet.write('G1', 'Date')

            # writes values from database down to spreadsheet
            for i, row in enumerate(res, 1):
                for j, value in enumerate(row):
                    print(i, j)
                    if row[6] == d:
                        worksheet.write(i, j, value)

            workbook.close()
            
            # deletes all records from database
            # after exporting to spreadsheet
            # self.delete = "DELETE FROM records"
            # self.cur.execute(self.delete)
        conn.commit()
        conn.close()



