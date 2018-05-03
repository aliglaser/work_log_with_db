import unittest
import datetime
from unittest.mock import Mock, patch
from playhouse.test_utils import test_database
from peewee import *
import sys
import work_log_db



TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([work_log_db.Entry], safe=True)

ENTRIES = [
    {
        'name': 'Max Planck',
        'task_name': 'Quantum mechanics',
        'time_spent': 10000,
        'notes': 'Nobel Prize in Physics in 1918',
        'timestamp': datetime.datetime(1919, 11, 13)
    },
    {
        'name': 'Niels Bohr',
        'task_name': 'Quantum mechanics and atomic structure',
        'time_spent': 20000,
        'notes': 'Nobel Prize in Physics in 1922.',
        'timestamp': datetime.date(1922, 12, 10)
    },
    {
        'name': 'Arieh Warshel',
        'task_name': 'Theoretical chemistry',
        'time_spent': 50000,
        'notes': 'Nobel Prize in Chemistry in 2013.',
        'timestamp': datetime.date(2013, 12, 8)
    },
    {
        'name': 'Max Kruse',
        'task_name': 'Forward',
        'time_spent': 6600,
        'notes': '',
        'timestamp': datetime.date(2013, 12, 8)
    },
]

class WorkLogEntryTests(unittest.TestCase):
	
	def test_name_entry(self):
		with unittest.mock.patch('builtins.input', return_value='alison'):
			assert work_log_db.name_entry() == 'alison'

	def test_task_name_entry(self):
		with unittest.mock.patch('builtins.input', return_value='math'):
			assert work_log_db.task_name_entry() == 'math'

	def test_time_spent_entry(self):
		with unittest.mock.patch('builtins.input', return_value=30):
			assert work_log_db.time_spent_entry() == 30			

	def test_notes_entry(self):
		with unittest.mock.patch('builtins.input', return_value="It has to be done by tmrw"):
			assert work_log_db.notes_entry() == "It has to be done by tmrw"


class WorkLogAddDeleteEditTests(unittest.TestCase):

	def test_add_entry(self):
		with unittest.mock.patch('builtins.input', side_effect=["alice", "project", 33333, "until May", " "]):		
			assert work_log_db.add_entry().name == "alice"

	def test_delete_entry(self):
		with test_database(TEST_DB, (work_log_db.Entry,)):
			entry = work_log_db.Entry.create(**ENTRIES[0])
			self.assertEqual(work_log_db.Entry.select().count(), 1)
			with unittest.mock.patch('builtins.input', return_value="y"):
				work_log_db.delete_entry(entry)
				self.assertEqual(work_log_db.Entry.select().count(), 0)

	def test_edit_entry(self):
		with test_database(TEST_DB, (work_log_db.Entry,)):
			entry = work_log_db.Entry.create(**ENTRIES[0])
			self.assertEqual(work_log_db.Entry.select().count(), 1)
			with unittest.mock.patch('builtins.input', side_effect=["coffee", "02/02/2002", "barista", 222, "Whatanice", "y", " "]):
				self.assertEqual(work_log_db.edit_entry(entry=entry).name, "coffee")			



class WorkLogSearchTests(unittest.TestCase):

	def test_find_by_employee(self):
		with test_database(TEST_DB, (work_log_db.Entry,)):
			entry = work_log_db.Entry.create(**ENTRIES[0])
			self.assertEqual(work_log_db.Entry.select().count(), 1)
			with unittest.mock.patch('builtins.input', return_value="Max Planck"):
				self.assertEqual(work_log_db.find_by_employee().count(), 1)		

	def test_find_by_term(self):
		with test_database(TEST_DB, (work_log_db.Entry,)):
			entry = work_log_db.Entry.create(**ENTRIES[0])
			self.assertEqual(work_log_db.Entry.select().count(), 1)
			with unittest.mock.patch('builtins.input', return_value="Quantum"):
				self.assertEqual(work_log_db.find_by_term().count(), 1)

	def test_find_by_time_spent(self):
		with test_database(TEST_DB, (work_log_db.Entry,)):
			entry = work_log_db.Entry.create(**ENTRIES[3])
			self.assertEqual(work_log_db.Entry.select().count(), 1)
			with unittest.mock.patch('builtins.input', return_value="6600"):
				self.assertEqual(work_log_db.find_by_time_spent().count(), 1)

	def test_find_by_date(self):
		with test_database(TEST_DB, (work_log_db.Entry,)):
			entry = work_log_db.Entry.create(**ENTRIES[3])
			self.assertEqual(work_log_db.Entry.select().count(), 1)
			with unittest.mock.patch('builtins.input', return_value="08/12/2013"):
				self.assertEqual(work_log_db.find_by_date().count(), 1)			

	def test_find_by_date_range(self):
	 	with test_database(TEST_DB, (work_log_db.Entry,)):
	 		entry = work_log_db.Entry.create(**ENTRIES[3])
	 		self.assertEqual(work_log_db.Entry.select().count(), 1)
	 		with unittest.mock.patch('builtins.input', side_effect=["01/01/2013", "01/01/2014", " ", " "]):
	 			self.assertEqual(work_log_db.find_by_date_range().count(), 1)			


if __name__ == '__main__':
    unittest.main()
