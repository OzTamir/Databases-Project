from __future__ import print_function
from config import Config
from database import *
from ui import UIBase

class ProjectUI(UIBase):
	''' UI For DB project '''
	def __init__(self, db, config):
		self.options = {1 : self.new_order, 2 : self.new_purchase}
		UIBase.__init__(self, db, config)

	def mainUI(self):
		''' Display a menu '''
		print('Choose an action:')
		print('1. Create a new order')
		print('2. Create a new purchase')
		print('3. Exit')
		choice = int(input('> '))
		if choice == 3:
			print('Goodbye!')
			return
		self.options.get(choice, self.print_error)()
		self.mainUI()

def main():
	conf = Config('config.json', True)
	db = Database(conf)
	ui = ProjectUI(db, conf)


if __name__ == '__main__':
	main()