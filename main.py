#!/usr/bin/python3
__version__=str(1.3)
__author__='bc03'
program_info=f'Simple Server inspector regards : {__author__}'
def get_args():
	import argparse
	parser=argparse.ArgumentParser(description=program_info)
	parser.add_argument('-v','--version',action='version',version=f'%(prog)s v{__version__}')
	parser.add_argument('url',help='Link to the website/API')
	parser.add_argument('-g','--get',help='Use GET method to send json data in path',metavar='path',)
	parser.add_argument('-p','--post',help='Use POST method to send json data in path',metavar='path')
	parser.add_argument('-c','--cookies',help='Path to cookies file formated in json',metavar='path')
	parser.add_argument('-o','--output',help="Path to save the response' contents",metavar='filepath')
	parser.add_argument('-t','--trials',help='Number of times to send request',type=int,default=1)
	parser.add_argument('-tbl','--table',help='Table format for displaying contents',metavar='[html,grid]+',choices=['html','grid','fancy_grid','orgtbl','pretty'])
	parser.add_argument('-wr','--write-mode',help='File mode for saving response',dest='write_mode',default='w',choices=['a','wb','ab'],metavar='[a,wb,ab]')
	parser.add_argument('-i','--interval',help='Time to sleep between requests sent',type=float,default=0)
	parser.add_argument('-thr','--thread',help='Threads amount at once',type=int)
	parser.add_argument('--binary',help='Specifies to handle response contents as binary data',action='store_true')
	parser.add_argument('--show',help='Displays the response contents',action='store_true',dest='all')
	parser.add_argument('--prettify',help='Formats the response in readable format',action='store_true')
	parser.add_argument('--new',help='Overwrites file with same name - output',action='store_true')
	return parser.parse_args()
args=get_args()
import cloudscraper
import colorama as col
from sys import argv 
from tabulate import tabulate
from time import sleep
from requests import Session
res=col.Fore.RESET
r=col.Fore.RED
b=col.Fore.BLUE
y=col.Fore.YELLOW
c=col.Fore.CYAN
g=col.Fore.GREEN
w=col.Fore.WHITE
m=col.Fore.MAGENTA
sess_ion=Session()
def exit_t(e='exiting...'):
	print(y+'ERROR : '+r+str(e)+res)
	from sys import exit
	exit()
def verify_write_mode():
	if args.binary:
		rp='wb'
	else:
		rp='w'
	return rp
def save_data(data):
	if args.output:
		try:
			with open(args.output,verify_write_mode() if args.new else args.write_mode ) as fp:
				fp.write(data)
		except Exception as e:
			print(f'[*] Failed to save data - {e}')
class output:
	def __init__(self):
		self.out=lambda a,b:print(f'[*] {str(a)+str(b)+res}')
	def info(self,msg):
		self.out(c,msg)
	def warn(self,msg):
		self.out(y,msg)
	def error(self,msg):
		self.out(r,msg)
class handler:
	def __init__(self):
		self.out=output()
		link=args.url
		if not 'http' in link:
			if 'localhost' in link or '192.' in link or '10.' in link or '127.' in link:
				link='http://' + link
			else:
				link='https://'+link
		self.link=link
	def data(self):
		try:
			pasr={'url':self.link}
			req=cloudscraper.create_scraper(sess=sess_ion)
			if args.cookies:
				from json import loads
				pasr['cookies']=loads(open(args.cookies).read())
			if args.post:
				from json import loads
				pasr['data']=loads(open(args.post).read())
				resp=req.post(**pasr)
			elif args.get:
				from json import loads
				pasr['params']=loads(open(args.get).read())
				resp=req.get(**pasr)
			else:
				resp=req.get(self.link)
		except Exception as e:
			exit_t(e)
		else:
			print(m+'Source : '+r+resp.url)
			return resp
	def header_info(self,resp):
		for key,value in resp.headers.items():
			sorted=f'{key.capitalize()} : {g}{value}{res}'
			if key.lower() in ['server']:self.out.warn(f'SERVER : {b+value+res}')
			else:self.out.info(sorted)
			#save_data(sorted)
	def main(self):
		try:
			resp=self.data()
		except Exception as e:
			exit_t(e)
		st_code=f'Status code : {g+str(resp.status_code)+" - "+y+resp.reason+res}'			
		self.out.warn(st_code)
		if args.table:
				data=[]
				for k,v in resp.headers.items():
					data.append([g+k.upper(),c+v])
				self.out.info('Header info!\n'+tabulate(data,headers=[y+'Header',y+'Info'],tablefmt=args.table))
		else:
				self.header_info(resp)		
		if args.all or args.output:
			#if not args.table:
				#self.header_info(resp)
			if args.prettify:
				from bs4 import BeautifulSoup as bts
				dta=bts(resp.text,'html.parser').prettify()
			else:
				dta=resp.content if args.binary else resp.text
			if args.all:
				self.out.info(f'{r} CONTENT {res}\n'+w+dta+res)
			if args.output:
					save_data(dta)
if __name__=='__main__':
	try:
		run=handler()
		if args.thread:
			from threading import Thread as thr
			x=0
			while x<args.trials+1:
				t1=thr(target=run.main,);
				t1.start();x+=1
				if x%args.thread==0:
					t1.join()
					sleep(args.interval)
		else:
			for _ in range(args.trials):
				run.main()
				try:
					wait=sleep(args.interval) if args.interval else None
				except Exception as e:
					exit_t(str(e,))
				print('',end='\n')
	except Exception as e:
		exit_t(str(e))
#12312204536
