# geo-temporal-generator
Randomly generate geospatial, temporal, continuous and discrete data in CSV format. The start date and time is output within a specified range; the latitude and longtitude coordinates are output within a specified extent; the continious and discrete data can be easily modified, the number of rows output can be specified.

Preview on google fusion tables:

[Fusion tables document](https://www.google.com/fusiontables/DataSource?docid=11o56wpO4PE1yuXCaQDlEtbuMKP90cbGg4NsTAQch)

[Fusion tables map](https://www.google.com/fusiontables/embedviz?q=select+col3%2C+col4+from+11o56wpO4PE1yuXCaQDlEtbuMKP90cbGg4NsTAQch+limit+1000&viz=HEATMAP&h=true&lat=53.32513175791224&lng=-6.1969757080078125&t=1&z=10&l=col3&y=7&tmplt=8&hmd=true&hmg=%2366ff0000%2C%2393ff00ff%2C%23c1ff00ff%2C%23eeff00ff%2C%23f4e300ff%2C%23f4e300ff%2C%23f9c600ff%2C%23ffaa00ff%2C%23ff7100ff%2C%23ff3900ff%2C%23ff0000ff&hmo=0.6&hmr=10&hmw=0&hml=TWO_COL_LAT_LNG)

[Fusion tables integer scatterplot](https://www.google.com/fusiontables/embedviz?containerId=googft-gviz-canvas&q=select+col1%2C+col6+from+11o56wpO4PE1yuXCaQDlEtbuMKP90cbGg4NsTAQch+order+by+col1+asc&viz=GVIZ&t=SCATTER&rmax=250&uiversion=2&gco_forceIFrame=true&gco_hasLabelsColumn=true&width=500&height=300)

##Usage:
```
$ ./georand.py -h
./georand.py <min datetime> <max datetime> <min lat> <min long> <max lat> <max long> <rows>
./georand.py "2000-01-01 00:00:00" "2015-12-21 23:59:00" 53.438528 -6.403656 53.196751 -6.099472 20
```
Note: The mathematics of the lat long values is not obvious, permitted latitude values must fall within the range -85.05113 and +85.05113, the permitted longtitude values fall within the range -179.999999999 and +179.999999999.

##Outputs:
```
Id,Startdate,Enddate,Latitude,Longtitude,Category,Integer,Float
0,2002-12-29 09:06:38,2003-04-04 09:06:38,53.2727969109,-6.12257493631,banana,266,0.564181956254
1,2013-05-28 01:22:31,2013-08-08 01:22:31,53.303376253,-6.24554711517,kiwi,263,0.678119433705
2,2006-03-30 14:18:58,2006-06-30 14:18:58,53.3513337935,-6.12931396636,orange,49,0.213356952542
3,2007-06-24 20:56:28,2007-06-30 20:56:28,53.373896141,-6.30834457249,lemon,344,0.131556437962
4,2008-11-12 19:47:58,2009-01-12 19:47:58,53.2771376894,-6.38116121,lemon,175,0.275158247104
5,2009-10-22 18:13:58,2010-01-14 18:13:58,53.3714053888,-6.28696865834,banana,263,0.257320162054
6,2014-03-19 08:19:16,2014-05-30 08:19:16,53.4371320156,-6.33167045358,orange,132,0.124539534804
7,2013-09-22 21:00:09,2013-11-28 21:00:09,53.35275974,-6.38387537616,orange,174,0.0937067873635
8,2010-10-11 03:41:43,2010-11-18 03:41:43,53.2358560207,-6.34108205064,kiwi,219,0.722678130093
9,2014-10-16 08:27:53,2014-12-30 08:27:53,53.1984975892,-6.35187268352,banana,48,0.897704825584
10,2006-07-14 19:27:26,2006-08-26 19:27:26,53.4256117187,-6.31552241218,apple,23,0.00519645632686
11,2001-10-11 01:57:33,2001-11-20 01:57:33,53.2830163047,-6.39485650889,apple,28,0.995039697194
12,2002-08-01 23:55:46,2002-09-04 23:55:46,53.4143523617,-6.23293140057,lemon,261,0.107784629623
13,2013-01-22 20:34:48,2013-05-02 20:34:48,53.2707436409,-6.18752934166,kiwi,211,0.0766004505737
14,2011-12-14 23:51:14,2012-01-09 23:51:14,53.2604935035,-6.33807302032,apple,201,0.347504904176
15,2001-01-30 12:54:47,2001-03-09 12:54:47,53.2893237657,-6.32681288614,kiwi,148,0.0174374936973
16,2004-06-02 04:14:08,2004-09-08 04:14:08,53.3067681004,-6.18778486725,apple,239,0.466909547646
17,2003-06-08 20:01:49,2003-09-11 20:01:49,53.2837843544,-6.16341580602,banana,89,0.730002564398
18,2009-04-05 20:10:05,2009-06-09 20:10:05,53.4092809498,-6.11408099593,banana,75,0.131390072968
19,2008-10-19 03:41:05,2008-11-16 03:41:05,53.4108747758,-6.33198578886,lemon,362,0.606297113853
```

##Creating Lines and Polygons:
Non-intersecting lines and polygons can easily be created from the resulting CSV file. To create the polygons import the CSV file into QGIS by clicking "Layer" -> "Add Layer" -> "Delimited Text Layer". To create polygons there are 2 steps. Create Polygons from Points by clicking "Vector" -> "Geometry Tools" -> "Voronoi Polygons". Then to remove the overlapping part of adjacent polygons click "Processing" -> "Toolbox" and type "Delete duplicate geometries". To create the lines, you must first create the polygons, then there are 3 steps to create non-intersecting lines. First click "Vector" -> "Geometry Tools" -> "Polygons to Lines". Second click "Vector" -> "Geoprocessing Tools" -> "Dissolve" -> "Dissolve All". Third click "Processing" -> "Toolbox" and type "Explode Lines", and run the "Explode Lines" algorithm. See the screenshot uploaded into the repository. The resulting lines and polygons can be exported to a CSV file by right clicking on the layer and pressing "Save As: file-name.csv" -> "Format: Comma Separated Value [CSV]",  "CRS: Layer CRS", "Skip attribute creation", "Layer Options, GEOMETRY: AS_WKT", "OK".

![QGIS Screenshot](/qgis-create-polygons-and-lines.png "QGIS Screenshot")
