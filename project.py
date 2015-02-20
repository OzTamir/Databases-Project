from __future__ import print_function
from core import System

def main():
	system = System('my_config.json')
	system.ui_manager()

if __name__ == '__main__':
	main()