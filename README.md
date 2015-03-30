# geo-temporal-generator
Randomly generate geospatial, temporal, continious and discrete data in CSV format. The start date and time is output within a specified range; the latitude and longtitude coordinates are output within a specified extent; the continious and discrete data can be easily modified, the number of rows output can be specified.

##Usage:
```
$ ./georand.py -h
./georand.py <min datetime> <max datetime> <min lat> <min long> <max lat> <max long> <rows>
./georand.py "2000-01-01 00:00" "2015-12-21 23:59" 53.438528 -6.403656 53.196751 -6.099472 20
```

##Outputs:
```
startdatetime enddatetime latitude longtitude discreteval continiousint continiousfloat
```
