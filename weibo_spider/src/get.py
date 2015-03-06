#encoding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import json
def tree():
    return defaultdict(tree)

def find_all(Element,xpath):
	temp=Element.find_elements_by_xpath(xpath)
	while len(temp)==0:
		temp=Element.find_elements_by_xpath(xpath)
		delay(10)
		pass

	return temp

#"好高兴"
max_page_of_weibo_search=20
class Fans:
	username=''
	userid=''
	sex=''
	useraddr=""
	data=['0','0','0']

class Forward:
	content=''
	username=''
	userid=''
	link=''
	time=''

class Comment:
	content=''
	time=''
	username=''
	userid=''

class Weibo_of_ones:
	content=""
	link=""
	username=""
	userid=""
	source_content=""
	source_link=""
	time=""
	stat=""

class Comment_of_weibo:
	content=""
	username=""
	userid=""
	time=''
	stat=''
	comments=[]
	forwards=[]


def delay(time):
	for i in range(time):
		for j in range(1000):
			for k in range(500):
				a=100*100

def login(my_driver):	#this function use to login from http://d.weibo.com
	print 'delay finnish!'
	log=find_all(my_driver,"//div[@id='pl_common_top']/div/div/div[@class='gn_position']/div[@class='gn_login']/ul/li/a")
	log_in=log[1]
	log_in.click()

	froms=find_all(my_driver,"//div[@class='right']")
	user=froms[0].find_elements_by_xpath("//input[@name='username']")
	user=user[0]
	user.click()
	user.send_keys('mymusise@sina.com')
	passwd=froms[0].find_elements_by_xpath("//input[@name='password']")
	passwd=passwd[0]
	passwd.click()
	passwd.send_keys('1262guochengxi.')
	passwd.send_keys(Keys.RETURN)
	pass

def login_2(my_driver,uname,upasswd):
	if uname=='':
		print "Please enter your username!"
		exit(0)
	if upasswd=='':
		print "Please enter your password!"
		exit(0)
	url="""http://weibo.com/login.php"""
	# url="""http://d.weibo.com/"""
	my_driver.get(url)
	username=find_all(my_driver,"//input[@name='username']")
	username[1].click()
	username[1].send_keys(uname)

	passwd=find_all(my_driver,"//input[@name='password']")
	print len(passwd)
	passwd[1].click()
	passwd[1].send_keys(upasswd)
	passwd[1].send_keys(Keys.RETURN)

	#wait a minite!
	temp2=find_all(my_driver,"//div[@id='v6_pl_leftnav_group']")
	pass

def get_one_info(my_driver,userid):
	url="""http://weibo.com/"""+userid
	my_driver.get(url)
	check=find_all(my_driver,"//div[@id='Pl_Core_UserInfo__5']/div/div[@class='PCD_person_info']/a/span")
	check[0].click()
	
	person_info_tab=find_all(my_driver,"//div[@id='Pl_Official_PersonalInfo__64']")

	person_menber_info=find_all(my_driver,"//div[@id='Pl_Core_T8CustomTriColumn__61']")
	print person_menber_info[0].text
	person_all_info=person_menber_info[0].text+person_info_tab[0].text
	return person_all_info
	pass

def get_one_fans_Or_attention(my_driver,userid,Idd):
	url="""http://weibo.com/"""+userid
	my_driver.get(url)
	check=find_all(my_driver,"//div[@id='Pl_Core_T8CustomTriColumn__3']")
	links=check[0].find_elements_by_xpath(".//td[@class='S_line1']")
	fans_link=links[Idd].find_element_by_xpath(".//a")
	fans_number=int(fans_link.find_element_by_xpath(".//strong").text)
	#That's no sence that if the fans of this guy less 100,so exit. 
	if(fans_number<21):
		return 0
	fans_link.click()

	fans_list_table=find_all(my_driver,"//div[@id='Pl_Official_HisRelation__66']/div/div/div")
	fans_all_page=fans_list_table[0].find_elements_by_xpath(".//div[@class='W_pages']/a")[-2]
	fans_all_page=int(fans_all_page.text)
	if fans_all_page>5:
		fans_all_page=5

	old_list=fans_list_table[0].find_elements_by_xpath(".//div[@class='W_pages']/a")
	fans=[]
	for page_number in range(1,fans_all_page+1):#click the next_page 4time
		current_url=my_driver.current_url
		page_addr=current_url.index('&')
		des_url=current_url[:page_addr]+"&page="+str(page_number)
		my_driver.get(des_url)

		fans_list_table=find_all(my_driver,"//div[@id='Pl_Official_HisRelation__66']/div/div/div")
		lists=find_all(my_driver,"//ul[@class='follow_list']/li")
		old_list=lists
		print len(lists)
		for li in lists:
			temp=Fans()
			temp.username=li.find_element_by_xpath(".//div[@class='info_name W_fb W_f14']/a").text
			temp.sex=li.find_element_by_xpath(".//div[@class='info_name W_fb W_f14']/a/i").get_attribute('class').split(' ')[1].split('_')[1]
			temp.id=li.find_element_by_xpath(".//div[@class='info_name W_fb W_f14']/a[@class='S_txt1']").get_attribute('usercard').split('=')[1]
			temp.useraddr=li.find_element_by_xpath(".//div[@class='info_add']/span").text
			datas=li.find_elements_by_xpath(".//div[@class='info_connect']/span")
			for i in range(len(datas)):
				temp.data[i]=datas[i].text
			print temp.username+"  "+temp.sex+"  "+temp.id+"  "+temp.useraddr+"  	"+temp.data[1]
			fans.append(temp)
	return fans
	pass

def load_footer_weibo(my_driver):
	delay(50)
	footer=find_all(my_driver,"//div[@class='footer_link clearfix']/dl/dt")
	footer[0].click()
	for i in range(10):
		# footer[0].send_keys(Keys.PAGE_DOWN)
		footer[0].click()
		delay(30)
	pass

def classify(weibo):
	temp=Weibo_of_ones()
	temp.content=weibo.find_element_by_xpath(".//div[@class='WB_text W_f14']").text
	weibo_footer=weibo.find_elements_by_xpath(".//div[@class='WB_from S_txt2']/a")[0]
	temp.link=weibo_footer.get_attribute('href').split('?')[0]
	temp.time=weibo_footer.text

	source=weibo.find_elements_by_xpath(".//div[@class='WB_feed_expand']")
	if len(source)==0:
		temp.source_content=""
		temp.source_link=""
	else:
		temp.source_content=source[0].find_elements_by_xpath(".//div[@class='WB_text']")[0].text
		temp.source_link=source[0].find_elements_by_xpath(".//div[@class='WB_from S_txt2']/a")[0].get_attribute('href')

	return temp
	pass

def get_one_weibo(my_driver,userid):
	url="""http://weibo.com/"""+userid
	my_driver.get(url)
	check=find_all(my_driver,"//div[@id='Pl_Core_T8CustomTriColumn__3']")
	links=check[0].find_elements_by_xpath(".//td[@class='S_line1']")
	weibo_link=links[2].find_element_by_xpath(".//a")
	weibo_number=int(weibo_link.find_element_by_xpath(".//strong").text)
	if weibo_number==0:
		return 0
	weibo_link.click()
	#press page_down
	load_footer_weibo(my_driver)

	#get weibo number list div
	page_list=find_all(my_driver,"//div[@class='W_pages']")
	#get weibos
	if len(page_list)==0:
		weibos_div=find_all(my_driver,"//div[@class='WB_feed_detail clearfix']")
		weibos=[]
		for weibo in weibos_div:
			weibos.append(classify(weibo))
	else:
		page_number=len(page_list[0].find_elements_by_xpath(".//span/div/ul/li"))	
		current_url=my_driver.current_url
		page_addr=current_url.index('&')
		url_front=current_url[:page_addr]
		url_back=current_url[page_addr:]
		for i in range(1,page_number+1):
			des_url=url_front+"&page="+str(i)+url_back
			my_driver.get(des_url)

			weibos_table=find_all(my_driver,"//div[@id='Pl_Official_MyProfileFeed__23']")
			print "begin load weibo"
			load_footer_weibo(my_driver)
			print "load weibo finish"
			weibos_div=find_all(my_driver,"//div[@class='WB_feed_detail clearfix']")
			weibos=[]
			for weibo in weibos_div:
				weibos.append(classify(weibo))
			print "weibos:"+str(len(weibos))
			print page_number
	return weibos
	pass

def get_weibo_comment(my_driver,link):#problem :to slowly
	my_driver.get(link)
	weibo=Comment_of_weibo()
	#check read to get
	all_info=find_all(my_driver,"//div[@class='WB_feed WB_feed_profile']")
	print 'geting stat'
	#get stat of weibo
	stat=my_driver.find_element_by_xpath("//div[@class='WB_feed_handle']")
	weibo.stat=stat.text
	#click is able to get comment of weibo
	comment_span=stat.find_elements_by_xpath(".//ul/li/a/span/span")[2]
	# comment_span.click()
	te=comment_span.text.split(' ')
	if len(te)!=1:#if have comment
		comments_table=find_all(my_driver,"//div[@node-type='feed_list']/div/div/div[@class='list_li S_line1 clearfix']")
		#get comment page number
		print "len:"+str(len(comments_table))
		comment_page=1
		comment_page_list=find_all(my_driver,"//div[@class='W_pages']")
		if len(comment_page_list)!=0:
			comment_page=int(comment_page_list[0].find_elements_by_xpath(".//a")[-2].text)
		print "comment_page_:"+str(comment_page)

		old_list=find_all(my_driver,"//div[@node-type='feed_list']")
		for i in range(comment_page):
		# for i in range(1):
			comments_table=find_all(my_driver,"//div[@node-type='feed_list']/div/div/div[@class='list_li S_line1 clearfix']")
			while comments_table[0]==old_list[0]:
				comments_table=find_all(my_driver,"//div[@node-type='feed_list']/div/div/div[@class='list_li S_line1 clearfix']")
			old_list=comments_table
			for comment in comments_table:
				temp=Comment()
				c_content=comment.find_elements_by_xpath(".//div[@class='list_con']/div[@class='WB_text']")[0].text
				temp.content=c_content
				
				temp.userid=comment.find_element_by_xpath(".//div[@class='WB_face W_fl']/a/img").get_attribute('usercard').split('=')[-1]
				
				
				temp.username=comment.find_elements_by_xpath(".//div[@class='WB_text']/a")[0].text
				
				temp.time=comment.find_elements_by_xpath(".//div[@class='WB_func clearfix']/div")[1].text
				print temp.username
				print temp.content
				print temp.userid
				print temp.time
				weibo.comments.append(temp)
			check_s=find_all(my_driver,"//div[@class='WB_repeat S_line1']")[1]
			next_a=check_s.find_elements_by_xpath("//div[@class='WB_cardpage S_line1']/div[@class='W_pages']/a/span")
			if len(next_a)>0:
				next_a[-1].click()

	#get Forward 
	stat=my_driver.find_element_by_xpath("//div[@class='WB_feed_handle']")
	forward_spans=stat.find_elements_by_xpath(".//ul/li/a/span/span")
	print 'finding to click!'
	print forward_spans[1].text
	te=forward_spans[1].text.split(' ')
	if len(te)>1:
		forward_spans[1].click()#click to forward

		#check ready to get forward

		print 'click finish!'

		check_s=find_all(my_driver,"//div[@class='WB_repeat S_line1']")[1]
		every_forward=check_s.find_elements_by_xpath(".//div[@class='list_ul']/div")
		while (len(every_forward)==0):
			check_s=find_all(my_driver,"//div[@class='WB_repeat S_line1']")[1]
			every_forward=check_s.find_elements_by_xpath(".//div[@class='list_ul']/div")
		#get forward page number
		forward_page=1
		forward_page_list=check_s.find_elements_by_xpath("//div[@class='WB_cardpage S_line1']/div[@class='W_pages']/a")
		if len(forward_page_list)!=0:
			forward_page=int(forward_page_list[-2].text)
		print "forward_page:"+str(forward_page)
		old_list=find_all(my_driver,"//div[@node-type='feed_list']")
		#get every page forward
		print "geting_forward"
		for i in range(forward_page):
			print "geting"
			check_s=find_all(my_driver,"//div[@class='WB_repeat S_line1']")[1]
			forward_table=check_s.find_elements_by_xpath(".//div[@class='list_li S_line1 clearfix']")
			old_list=forward_table
			for comment in forward_table:
				temp_f=Forward()
				user=comment.find_elements_by_xpath(".//div[@class='WB_text']/a")[0]
				temp_f.username=user.text
				temp_f.userid=user.get_attribute('usercard').split('=')[-1]
				temp_f.connet=comment.find_elements_by_xpath(".//div[@class='WB_text']/span")[0].text
				temp_f.link=comment.find_elements_by_xpath(".//div[@class='WB_from S_txt2']/a")[0].get_attribute('href')
				temp_f.time=comment.find_elements_by_xpath(".//div[@class='WB_from S_txt2']/a")[0].text
				print temp_f.username
				print temp_f.userid
				print temp_f.connet
				print temp_f.link
				weibo.forwards.append(temp_f)
				pass
			next_a=check_s.find_elements_by_xpath("//div[@class='WB_cardpage S_line1']/div[@class='W_pages']/a/span")
			if len(next_a)>0:
				next_a[-1].click()
			pass

	print weibo.content	
	print weibo.stat
	return weibo
	pass

def get_search(my_driver,key_word):
	my_driver.get("http://d.weibo.com")
	top=find_all(my_driver,"//div[@id='pl_common_top']")
	search_input=top[0].find_elements_by_xpath(".//div[@class='gn_search']/input")
	search_input[0].click()
	search_input[0].send_keys(key_word)
	search_input[0].send_keys(Keys.RETURN)
	#click to just search weibo
	head_div=find_all(my_driver,"//div[@id='pl_common_searchTop']")
	weibo_click=head_div[0].find_elements_by_xpath(".//ul[@class='formbox_tab clearfix formbox_tab2']/li/a")
	weibo_click[1].click()
	#check click finish
	check_i=find_all(my_driver,"//div[@id='pl_wb_feedlist']")
	#get number
	number_list=find_all(my_driver,"//div[@class='WB_cardwrap S_bg2 relative']")
	page_number=1
	if len(number_list)!=0:
		page_number=len(number_list[0].find_elements_by_xpath(".//span[@class='list']/div/ul/li"))
	print page_number
	if page_number>max_page_of_weibo_search:
		page_number=max_page_of_weibo_search
	#get weibo
	weibos=[]
	for i in range(page_number-1):
	# for i in range(1):
		every_weibo=find_all(my_driver,"//div[@class='WB_cardwrap S_bg2 clearfix']")
		print len(every_weibo)

		#get every weibo
		for e in every_weibo:
			temp=Weibo_of_ones()
			user=e.find_elements_by_xpath(".//div[@class='feed_content wbcon']/a")[0]
			temp.username=user.text
			temp.userid=user.get_attribute('href').split('/')[-1]
			temp.content=e.find_elements_by_xpath(".//div[@class='feed_content wbcon']/p")[0].text
			t_l=e.find_elements_by_xpath(".//div[@class='feed_from W_textb']/a")[0]
			temp.time=t_l.text
			temp.link=t_l.get_attribute('href')
			print temp.username
			print temp.userid
			print temp.content
			print temp.time+" "+temp.link
			weibos.append(temp)
		#click next page
		if page_number>1:
			delay(200)
			number_list=find_all(my_driver,"//div[@class='WB_cardwrap S_bg2 relative']")
			print "here:"+str(len(number_list))
			next_a=number_list[0].find_elements_by_xpath(".//a[@class='page next S_txt1 S_line1']")
			next_a[0].click()
	#check
	return weibos
	pass

def main():
	my_driver = webdriver.Firefox()
	login_2(my_driver,'mymusise','1262guochengxi')
	# print get_one_info(my_driver,'oxian')
	# get_one_fans(my_driver,'3173516772')
	get_one_fans_Or_attention(my_driver,'3173516772',1)
	# print get_one_weibo(my_driver,'3173516772')
	# temp=get_weibo_comment(my_driver,"http://weibo.com/1918656457/Br1qVpOku")

	'''
	weibos=get_search(my_driver,"滴滴打车".decode('utf-8'))
	f=open("data.json",'w')
	data=tree()
	i=0
	for weibo in weibos:
		data[i]['username']=weibo.username
		data[i]['userid']=weibo.userid
		data[i]['content']=weibo.content
		data[i]['link']=weibo.link
		data[i]['time']=weibo.time
		i=i+1
	f.write(json.dumps(data))
	'''

if __name__ == '__main__':
	main()