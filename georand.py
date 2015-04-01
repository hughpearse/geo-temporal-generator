#!/bin/python

import sys, getopt, random, string, datetime
import re
from datetime import timedelta
from datetime import datetime
from random import randint

def random_date(start, end):
	return start + timedelta(
		seconds=randint(0, int((end - start).total_seconds())))

def show_help():
	print './georand.py <min datetime> <max datetime> <min lat> <min long> <max lat> <max long> <rows>'
	print './georand.py "2000-01-01 00:00:00" "2015-12-31 23:59:59" 53.438528 -6.403656 53.196751 -6.099472 20'
	print 'Outputs: id,startdatetime,enddatetime,latitude,longtitude,discreteval,dichotomousval,continiousint,continiousfloat,"text"'

def main(argv):
	
	discretedata = ['apple','orange','banana','lemon','kiwi']
	
	try:
		opts, args = getopt.getopt(argv,"h",["help"])
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	for opt, arg in opts:
		if (opt == '-h') or (opt == '--help'):
			show_help()
			sys.exit()
	if (len(sys.argv) == 1):
		show_help()
		sys.exit(0)
	
	mindatetime = str(sys.argv[1])
	maxdatetime = str(sys.argv[2])
	minlat = float(sys.argv[3])
        minlong = float(sys.argv[4])
        maxlat = float(sys.argv[5])
        maxlong = float(sys.argv[6])
	rows = int(sys.argv[7])
	
	print "Id,Startdate,Enddate,Latitude,Longtitude,Category,Bool,Integer,Float,Text"
	
	for num in range(0,rows):
		d1 = datetime.strptime(mindatetime, '%Y-%m-%d %H:%M:%S')
		d2 = datetime.strptime(maxdatetime, '%Y-%m-%d %H:%M:%S')
		randdate = random_date(d1, d2)
		enddate = randdate + timedelta(days=randint(0,365), hours=randint(0,24), minutes=randint(0,60), seconds=randint(0,60))
	
		lat = random.uniform(minlat,maxlat)
		long = random.uniform(minlong,maxlong)
		
		discreteval = ''.join(random.choice(discretedata))
		continuousint = randint(0,100)
		continiousfloat = random.random()
		dichotomousval = random.choice(['true','false'])
		randomtext = ''.join([random.choice(string.ascii_lowercase + ' '*8 + 'aeiou'*8) for n in xrange(randint(16,56))]).lstrip().rstrip()
		randomtext = re.sub(' +', ' ', randomtext)

		#print "%s%s%s%s%s" % (randdate,',',lat,',',long)
		#print "%s%s%s%s" % ('http://www.openstreetmap.org/#map=16/',lat,'/',long)
		print "%s,%s,%s,%s,%s,%s,%s,%s,%s,\"%s\"" % (num,randdate,enddate,lat,long,discreteval,dichotomousval,continuousint,continiousfloat,randomtext)

if __name__ == "__main__":
	main(sys.argv[1:])
