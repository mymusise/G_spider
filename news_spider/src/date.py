#encoding:utf-8
class NewsDate:
	month=0
	day=0
	hour=0
	minute=0
	def __init__(self,string):
		string=string.replace('(','').replace(')','')
		string=string.split(' ')
		self.month=int(string[0][:2])
		self.day=int(string[0][5:7])
		self.hour=int(string[1].split(':')[0])
		self.minute=int(string[1].split(':')[1])
	def disPlay(self):
		print str(self.month)+"-"+str(self.day)+" "+str(self.hour)+":"+str(self.minute)
		pass
	def day_compare(self,other_date):
		if self.month*30+self.day<other_date.month*30+other_date.day :
			return -1
		elif self.month*30+self.day>other_date.month*30+other_date.day:
			return 1
		elif self.month*30+self.day==other_date.month*30+other_date.day:
			return 0
		pass
	def time_compare(self,other_date):
		if self.hour*60+self.minute<other_date.hour*60+other_date.minute:
			return -1
		elif self.hour*60+self.minute>other_date.hour*60+other_date.minute:
			return 1
		else:
			return 0
	def compare(self,other_date):
		if self.day_compare(other_date)==-1:
			return  -1
		elif self.day_compare(other_date)==1:
			return 1
		elif self.day_compare(other_date)==0 and self.time_compare(other_date)==-1:
			return -1
		elif self.day_compare(other_date)==0 and self.time_compare(other_date)==1:
			return 1
		else:
			return 0
		pass
def main():
	date1=NewsDate("(01月15日 16:54)")
	date2=NewsDate("(01月15日 16:54)")
	date1.disPlay()
	date2.disPlay()
	print date2.compare(date1)
	pass
if __name__ == '__main__':
	main()