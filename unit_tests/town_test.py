# -*- coding: utf-8 -*-

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import town
import unittest
from datetime import date, datetime, timedelta

class TownTest(unittest.TestCase):

    def setUp(self):
        variables = {'form_name':'unit testing',
                'session_user_var_zipcode':'5032',
                'session_user_var_birthplace':'iMio',
                'session_user_var_title':'Title',
                'form_objects':'objects'}
        self.commune = town.Town(variables)

    def test_diff_dates_input_as_string(self):
        today = date.today()
        yesterday = (today - timedelta(days=1)).strftime('%d/%m/%Y')
        today = today.strftime('%d/%m/%Y')
        
        self.assertEqual(self.commune.diff_dates(today, yesterday), "1") 
        self.assertEqual(self.commune.diff_dates(yesterday, today), "1")

    def test_diff_dates_input_as_datetime(self):
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        
        self.assertEqual(self.commune.diff_dates(today, yesterday), "1") 
        self.assertEqual(self.commune.diff_dates(yesterday, today), "1")

    def test_diff_dates_input_as_date(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        self.assertEqual(self.commune.diff_dates(today, yesterday), "1") 
        self.assertEqual(self.commune.diff_dates(yesterday, today), "1")
  
if __name__ == '__main__':
        unittest.main() 