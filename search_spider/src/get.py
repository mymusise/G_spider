#encoding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import json

class SearchResult():
	title=''
	link=''
	content=''
	pass

page_number_of_result=5

def tree():
	return defaultdict(tree)

def get_a_page(my_driver,url):
	i=1
	while i:
		try:
			print 'getting a new page...'
			my_driver.get(url)
			i=0
			print 'finish!'
		except:
			my_driver.refresh()
			print 'false!refreshing...'

def delay(time):
	for i in range(time):
		for j in range(1000):
			for k in range(500):
				pass

def find_all(Element,xpath):
	temp=Element.find_elements_by_xpath(xpath)
	while len(temp)==0:
		temp=Element.find_elements_by_xpath(xpath)
		delay(10)
		pass

	return temp

def just_find(Element,xpath):
	temp=Element.find_elements_by_xpath(xpath)
	return temp

def get_google_search(str):
	myProxy = "127.0.0.1:8087"
	proxy = Proxy({
	'proxyType': ProxyType.MANUAL,
	'httpProxy': myProxy,
	'ftpProxy': myProxy,
	'sslProxy': myProxy,
	'noProxy': '' # set this value as desired
	})
	# profile = webdriver.FirefoxProfile()
	# profile.set_preference("network.proxy.type", 1)
	# profile.set_preference("network.proxy.http", "127.0.0.1")
	# profile.set_preference("network.proxy.http_port", 8087)
	# profile.accept_untrusted_certs = True
	# profile.update_preferences()

	my_driver=webdriver.Firefox(proxy=proxy)
	my_driver.set_page_load_timeout(20)
	# my_driver=webdriver.PhantomJS()
	get_a_page(my_driver,"https://www.google.com.hk")
	#search the key word
	key_input=find_all(my_driver,"//input[@id='lst-ib']")[0]
	key_input.send_keys(str)
	key_input.send_keys(Keys.RETURN)
	#get the result
	old_url=" "
	all_result=[]
	for i in range(page_number_of_result):
		result_srg=find_all(my_driver,"//div[@class='srg']/li")
		print len(result_srg)
		for result in result_srg:
			temp=SearchResult()
			temp.title=just_find(result,".//h3[@class='r']/a")[0].text
			temp.link=just_find(result,".//h3[@class='r']/a")[0].get_attribute('href')
			temp.content=just_find(result,".//div[@class='s']/div/span")[0].text
			print temp.title
			print temp.link
			print temp.content
			all_result.append(temp)
		#click the next page
		print 'finding next'
		next_ps=just_find(my_driver,"//table[@id='nav']/tbody/tr/td/a")
		print 'find next finish'
		if len(next_ps)==0 or len(next_ps)==1:
			break
		else:
			next_p=next_ps[-1]
			next_p.click()
			print 'waiting'
			while old_url==my_driver.current_url:
				pass
			old_url=my_driver.current_url
	my_driver.close()
	return all_result

def get_baidu_search(str):
	my_driver=webdriver.Firefox()
	get_a_page(my_driver,"http://www.baidu.com")
	#search key word
	key_input=find_all(my_driver,"//input[@id='kw']")[0]
	key_input.send_keys(str)
	key_input.send_keys(Keys.RETURN)
	#get the result of search
	old_url=""
	old_result_div=find_all(my_driver,"//div[@id='content_left']")
	all_result=[]
	for i in range(page_number_of_result):
		#check whether the page has changed
		result_div=find_all(my_driver,"//div[@id='content_left']/div[@class='result c-container ']")
		while result_div[0]==old_result_div[0]:
			result_div=find_all(my_driver,"//div[@id='content_left']/div[@class='result c-container ']")
		old_result_div=result_div
		print len(result_div)
		for result in result_div:
			temp=SearchResult()
			temp.title=just_find(result,".//h3[@class='t']/a")[0].text
			temp.link=just_find(result,".//h3[@class='t']/a")[0].get_attribute('href')
			temp.content=just_find(result,".//div[@class='c-abstract']")[0].text
			print temp.title
			print temp.link
			print temp.content
			all_result.append(temp)
		#click the next page
		next_ps=just_find(my_driver,"//div[@id='page']/a[@class='n']")
		if len(next_ps)==0:
			break
		else:
			next_p=next_ps[-1]
			next_p.click()
			while old_url==my_driver.current_url:
				pass
			old_url=my_driver.current_url
	my_driver.close()
	return all_result
	pass

def test():
	# get_google_search('python')
	get_baidu_search('python')
	pass

if __name__ == '__main__':
	test()