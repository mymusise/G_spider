#encoding:utf-8
from collections import defaultdict
import json
import uniout
from get import *
def tree():
    return defaultdict(tree)
def main():
	temp=tree()
	temp[1]
	temp[1]['username']='滴滴打车'
	temp[1]['userid']='12342433'

	print str(json.dumps(temp)).decode('utf-8').encode('utf-8')
	pass

def test():
	f=open('temp.json','r')
	s=f.read()
	js= json.loads(s)
	print js['2']['username'].encode('utf-8')
	pass
def test1():
	my_driver=webdriver.Firefox()
	login_2(my_driver,'mymusise@sina.com','1262guochengxi.')
	get_weibo_comment(my_driver,'http://weibo.com/2846859150/BFe3qr2oG')
if __name__ == '__main__':
	test1()