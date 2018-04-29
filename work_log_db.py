import sys
from collections import OrderedDict
import datetime
import os 


from peewee import *

db = SqliteDatabase('work_log.db')


def clear():
	os.system('cls' if os.name=="nt" else 'clear')	


class Entry(Model):
	name = TextField()
	task_name = TextField()
	time_spent = IntegerField(default=0)
	notes = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = db


def initialize():
	"""Create the database if they don't exist"""
	db.connect()
	db.create_tables([Entry], safe=True)


def name_entry():
    """Prompt the employee for their name."""
    """
	
	>>> name = name_entry()
	Enter a name: alison

    """
    while True:
        name = input("Enter a name: ")
        if len(name) == 0:
            print("\nPlease give us a name!\n")
            continue
        else:
            return name


def task_name_entry():
    """Prompt the task name."""
    """

	>>> task_name = task_name_entry()
	Enter a task name: korean study

    """
    while True:
        task_name = input("Enter a task name: ")
        if len(task_name) == 0:
            print("\nPlease give us a task name!\n")
            continue
        else:
            return task_name


def time_spent_entry():
    """Prompt the employee for the time spent on their task."""
    """

	>>> time_spent = time_spent_entry()
	Enter number of minutes spent working on the task: 20

    """
    while True:
        time_spent = input("Enter number of minutes spent working on the task: ")
        try:
            int(time_spent)
        except ValueError:
            print("\nNot a valid time entry! Enter time as a whole integer.\n")
            continue
        else:
            return time_spent



def notes_entry():
    """Prompt employee to provide any additional notes"""

    """

	>>> notes = notes_entry()
	Notes for this task (ENTER if None): by may 5th

    """
    notes = input("Notes for this task (ENTER if None): ")
    return notes



def add_entry():
	"""Add Entry"""

	"""

	>>> add_entry()
	Enter a name: alison
	Enter a task name: korean study
	Enter number of minutes spent working on the task: 20
	Notes for this task (ENTER if None): by june 2nd

	"""
	name = name_entry()
	task_name = task_name_entry()
	time_spent = time_spent_entry()
	notes = notes_entry()
	Entry.create(name = name, task_name=task_name, time_spent=time_spent, notes = notes)



def menu_loop():
	"""Show the menu"""
	
	"""

	>>>menu_loop()
	a) Add Entry
	b) Search entries
	Enter 'q' to quit.
	Action: a
	Enter a name: alpha
	Enter a task name: make a whole cake
	Enter number of minutes spent working on the task: 30
	Notes for this task (ENTER if None): hi

	"""
	while True:
		clear()
		for key, value in menu.items():
			print('{}) {}'.format(key, value.__doc__))
		print("Enter 'q' to quit.")
		choice = input('Action: ').lower()
		if choice.lower() == 'q':
			sys.exit("************Good bye************")
		if choice in menu:
			clear()
			menu[choice]()
		else:
			input("********Please choose the right one. Hit Enter/return to continue********")
			menu_loop()
		

def find_by_employee():
	"""Find by Employee"""
	"""
	
	>>> find_by_employee()
	****NAME LIST****
	lala
	nurinuri
	andrew souvlakii
	q
	q
	alison
	alpha
	Choose the name of the employee >> q
	======================================
	 Date: 04/28/2018
	 Employee name: q
	 Task: skip
	 Duration: 20
	 Notes: 1

	=======================================
	d) Delete an entry
	e) Edit the entry
	choose the menu(Hit enter to skip): 


	"""
	print("****NAME LIST****")
	employee_list = []
	employees  = Entry.select()
	for employee in employees:
		employee_list.append(employee.name)
	for employee in employee_list:
		print(employee)	
	print("*********************")	
	employee_name = input("Choose the name of the employee >> ")
	if employee_name in employee_list:
		entries = Entry.select().where(Entry.name.contains(employee_name))
		for entry in entries:
			clear()
			print("======================================")
			print('\n Date: ' + entry.timestamp.strftime("%m/%d/%Y") +
		'\n Employee name: ' + entry.name +
		'\n Task: ' + entry.task_name +
		'\n Duration: ' + str(entry.time_spent) +
		'\n Notes: '+ entry.notes+'\n')
			print("=======================================")
			after_choice(entry)
	else:
		print("===============")
		print("     None")	
		input("===============")
		


def find_by_date():
	"""Find by date"""
	"""

	>>> find_by_date()
	****DATE LIST****
	02/02/2019
	28/04/2018
	28/04/2018
	28/04/2018
	28/04/2018
	28/04/2018
	28/04/2018
	Select the date(DD/MM/YYYY) >> 02/02/2019 

	"""
	print("****DATE LIST****")
	date_list = []
	entries = Entry.select()
	for entry in entries:
		date_list.append(entry.timestamp.strftime("%d/%m/%Y"))		
	for date in date_list:
		print(date)	
	while True:
		date_fmt=input("Select the date(DD/MM/YYYY) >> ")
		try:
			exact_date_log = datetime.datetime.strptime(date_fmt, "%d/%m/%Y")
		except ValueError:
			input("*******Not The Right Format. Hit Enter to Continue*****")
			continue
		else:
			if date_fmt in date_list:
				print("==============================================")
				for entry in entries:
					if entry.timestamp.strftime("%d/%m/%Y") == date_fmt:
						print('\n Date: ' + entry.timestamp.strftime("%d/%m/%Y") +
	'\n Employee name: ' + entry.name +
	'\n Task: ' + entry.task_name +
	'\n Duration: ' + str(entry.time_spent) +
	'\n Notes: '+ entry.notes +'\n')
						after_choice(entry)
						(print("=============================================="))
				break
			else:
				print("===============")
				print("     None")	
				input("===============")
				break		
			
def delete_entry(entry):
	"""Delete an entry"""
	if input("Are you sure? [y/N] ").lower() == 'y':
		entry.delete_instance()
		input("Entry deleted Please hit Enter to proceed")

def edit_date_entry():
	date_fmt = input("Provide a changed date (dd/mm/YYYY)>> ")
	try:
		date_result = datetime.datetime.strptime(date_fmt, '%d/%m/%Y')
	except ValueError:
		print("Please provide one with the right form")
		edit_date_entry()
	else:
		return date_result		


def edit_entry(entry):
	"""Edit the entry"""
	edit_name = name_entry()
	edit_date = edit_date_entry()
	edit_task_name = task_name_entry()
	edit_time_spent = time_spent_entry()
	edit_notes = notes_entry()
	if input("Are you sure? [y/N] ").lower() == 'y':
		entry.name = edit_name
		entry.timestamp = edit_date
		entry.task_name = edit_task_name
		entry.time_spent = edit_time_spent
		entry.notes = edit_notes
		entry.save()
		input("Entry deleted Please hit Enter to proceed")
		

after_menu = OrderedDict([
	('d', delete_entry),
	('e', edit_entry),
])

def after_choice(entry):
	"""Choose to either delete or edit the entry"""

	for key, value in after_menu.items():
		print('{}) {}'.format(key, value.__doc__))
	choice = input('choose the menu(Hit enter to skip): ').lower()

	if choice in after_menu:
		clear()
		after_menu[choice](entry)
		
			

def find_by_time_spent():
	"""find_by_time_spent"""

	"""

	>>> find_by_time_spent()
	****SPENT TIME LIST*****
	20
	20
	34
	20
	20
	20
	30
	29
	Give us the time spent >> 20

	 Date: 02/02/2019
	 Employee name: lala
	 Task: k
	 Duration: 20
	 Notes: 

	d) Delete an entry
	e) Edit the entry
	choose the menu(Hit enter to skip): 

	"""
	print("****SPENT TIME LIST*****")
	time_spent_list = []
	entries = Entry.select()
	for entry in entries:
		time_spent_list.append(entry.time_spent)
	for time in time_spent_list:
		print(time)	
	while True:
		try:
			time_spent_input = int(input("Give us the time spent >> "))
		except ValueError:
			input("*******Not The Right Format. Hit Enter to Continue*****")
			continue
		else:
			if time_spent_input in time_spent_list:
				entries = Entry.select().where(Entry.time_spent == time_spent_input)
				for entry in entries:
					print('\n Date: ' + entry.timestamp.strftime("%m/%d/%Y") +
	'\n Employee name: ' + entry.name +
	'\n Task: ' + entry.task_name +
	'\n Duration: ' + str(entry.time_spent) +
	'\n Notes: '+ entry.notes+'\n')
					after_choice(entry)	
				break
			else:
				print("==========================")	
				print("          NONE")
				input("==========================")
				break			

def find_by_term():
	"""Find by term"""
	
	"""

	>>> find_by_term()
	Give us the term you're looking for >> lol
	==========================
          NONE
	==========================

	"""

	term = input("Give us the term you're looking for >> ")
	entries = Entry.select().where((Entry.task_name.contains(term))
		|(Entry.notes.contains(term)))
	for entry in entries:
		print('\n Date: ' + entry.timestamp.strftime("%m/%d/%Y") +
'\n Employee name: ' + entry.name +
'\n Task: ' + entry.task_name +
'\n Duration: ' + str(entry.time_spent) +
'\n Notes: '+ entry.notes+'\n')
		after_choice(entry)
	if entries == None:
		print("==========================")	
		print("          NONE")
		input("==========================")


def find_by_date_range():
	"""Find by date range"""

	"""
	
	>>> find_by_date_range()
	start date (MM/DD/YYYY)>> 02/09/2019
	end date (MM/DD/YYYY)>> 02/09/2022 
	==========================
	          NONE
	==========================


	"""
	start_date_str = input("start date (MM/DD/YYYY)>> ")
	start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y")
	end_date_str = input("end date (MM/DD/YYYY)>> ")
	end_date = datetime.datetime.strptime(end_date_str, "%m/%d/%Y")
	entries = Entry.select().where(((Entry.timestamp)>start_date)
		&(Entry.timestamp<end_date))
	for entry in entries:
		print('\n Date: ' + entry.timestamp.strftime("%m/%d/%Y") +
'\n Employee name: ' + entry.name +
'\n Task: ' + entry.task_name +
'\n Duration: ' + str(entry.time_spent) +
'\n Notes: '+ entry.notes+'\n')
	if entries == None:
		print("==========================")	
		print("          NONE")
		input("==========================")



search_menu = OrderedDict([
    ('e', find_by_employee),
    ('d', find_by_date),
    ('r', find_by_date_range),
    ('t', find_by_time_spent),
    ('k', find_by_term),
    ('q', menu_loop)
])


def search_entries():
	"""Search entries"""

	"""
	>>> search_entries()
	e) Find by Employee
	d) Find by date
	r) Find by date range
	t) find_by_time_spent
	k) Find by term
	q) Show the menu
	Search By: l
	********Please choose the right one. Hit Enter/return to continue********


	"""
	for key, value in search_menu.items():
		print('{}) {}'.format(key, value.__doc__))
	choice = input('Search By: ').lower()

	if choice in search_menu:
		clear()
		search_menu[choice]()
	else:
		input("********Please choose the right one. Hit Enter/return to continue********")
		search_entries()





menu = OrderedDict([
	('a', add_entry),
	('b', search_entries),
])



if __name__ == '__main__':
	initialize()
	menu_loop()

