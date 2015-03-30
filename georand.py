#!/bin/python

import sys, getopt, random, string, datetime
from datetime import timedelta
from datetime import datetime
from random import randint


def random_date(start, end):
	return start + timedelta(
		seconds=randint(0, int((end - start).total_seconds())))

def main(argv):
	
	try:
		opts, args = getopt.getopt(argv,"h",["help"])
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	for opt, arg in opts:
		if (opt == '-h') or (opt == '--help'):
			print './georand.py <min datetime> <max datetime> <min lat> <min long> <max lat> <max long> <rows>'
			print './georand.py "2000-01-01 00:00" "2015-12-21 23:59" 53.438528 -6.403656 53.196751 -6.099472 20'
			print 'Outputs: id randomdatetime enddatetime randomlatitude randomlongtitude randomdiscreteval randomcontiniousint randomcontiniousfloat'
			sys.exit()
	
	mindatetime = str(sys.argv[1])
	maxdatetime = str(sys.argv[2])
	minlat = float(sys.argv[3])
        minlong = float(sys.argv[4])
        maxlat = float(sys.argv[5])
        maxlong = float(sys.argv[6])
	rows = int(sys.argv[7])
	
	for num in range(0,rows):
		d1 = datetime.strptime(mindatetime, '%Y-%m-%d %H:%M')
		d2 = datetime.strptime(maxdatetime, '%Y-%m-%d %H:%M')
		randdate = random_date(d1, d2)
		enddate = randdate + timedelta(days=randint(0,365))
	
		lat = random.uniform(minlat,maxlat)
		long = random.uniform(minlong,maxlong)
		
		#discreteval = ''.join(random.choice(string.lowercase) for x in range(1))
		discreteval = ''.join(random.choice(['apple', 'orange', 'banana', 'lemon', 'kiwi']))
		continuousint = randint(0,100)
		continiousfloat = random.random()
		
		#print "%s%s%s%s%s" % (randdate,',',lat,',',long)
		#print "%s%s%s%s" % ('http://www.openstreetmap.org/#map=16/',lat,'/',long)
		print "%s,%s,%s,%s,%s,%s,%s,%s" % (num,randdate,enddate,lat,long,discreteval,continuousint,continiousfloat)

if __name__ == "__main__":
	main(sys.argv[1:])
