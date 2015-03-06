#encoding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import *

def get_a_page(my_driver,url):
	i=1
	while i:
		try:
			print 'getting'
			my_driver.get(url)
			i=0
			print 'finish'
		except:
			my_driver.refresh()
			print 'unfinish'

def main():
	my_driver=webdriver.Firefox()
	my_driver.set_page_load_timeout(1)
	get_a_page(my_driver,"https://www.dnspod.cn/Plans/Buy#personal")
	pass

if __name__ == '__main__':
	main()