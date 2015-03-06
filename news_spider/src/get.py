#encoding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
from date import *
import json

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
	pass

def get_list(my_driver):
	url="""http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_1.shtml"""
	f=open('progress.data','r')
	start_time= f.readline().split('::')[1].replace('\n','')
	end_time=f.readline().split('::')[1]
	f.close()
	start_date=NewsDate(start_time)
	end_date=NewsDate(end_time)
	start_date.disPlay()
	end_date.disPlay()
	get_a_page(my_driver,url)
	
	page_id=1
	exit_id=0
	page_link=[]
	begin_url=my_driver.current_url
	print begin_url
	old_list=find_all(my_driver,"//div[@id='T_Menu_01']")
	while exit_id==0:
		id_addr=begin_url.index('_')
		url=begin_url[:id_addr+1]+str(page_id)+begin_url[id_addr+2:]
		get_a_page(my_driver,url)
		while my_driver.current_url!=url:
			pass
		print my_driver.current_url
		lists=find_all(my_driver,"//ul[@class='list_009']/li")
		old_list=lists
		print len(lists)
		print page_id
		for lis in lists:
			link=find_all(lis,".//a")[0].get_attribute('href')
			time=NewsDate(find_all(lis,".//span")[0].text.encode('utf-8'))
			if time.compare(start_date)==-1:
				exit_id=1
				break
			if time.compare(start_date)==1 and time.compare(end_date)==-1:
				time.disPlay()
				page_link.append(link)
		page_id+=1
		pass
	return page_link
def get_news_info(my_driver,page_link):
	page_id=1
	f=open('progress.data','r')
	start_time= f.readline().split('::')[1].replace('\n','')
	end_time=f.readline().split('::')[1]
	for lis in page_link:
		if page_id%10==0:
			my_driver.close()
			my_driver=webdriver.Firefox()
			# my_driver=webdriver.PhantomJS()
			page_id+=1
		get_a_page(my_driver,lis)
		Title=find_all(my_driver,"//h1[@id='artibodyTitle']")[0].text
		time_source=find_all(my_driver,"//div[@class='wrap-inner']/div[@class='page-info']/span[@class='time-source']")[0].text
		content=find_all(my_driver,"//div[@id='artibody']")[0].text
		try:
			key_word=find_all(my_driver,"//div[@class='article-keywords']")[0].text
		except:
			key_word=" "
		# print time_source
		print Title
		# print content
		# print key_word
		f=open("../data/"+start_time+"--"+end_time,'a')
		f.write("\n<!--\n")
		f.write("Title:"+Title.encode('utf-8')+'\n')
		f.write("Time:"+time_source.encode('utf-8')+'\n')
		f.write("Content:"+content.encode('utf-8')+'\n')
		f.write("Key word:"+key_word.encode('utf-8')+'\n')
		f.write("\n--!>\n")
		f.close()
		page_id+=1

def main():
	my_driver=webdriver.Firefox()
	# my_driver=webdriver.PhantomJS()
	my_driver.set_page_load_timeout(15)
	lists=get_list(my_driver)
	get_news_info(my_driver,lists)
	pass

if __name__ == '__main__':
	main()