#!/bin/python

#points imports
import sys, getopt, random, string, datetime
import re
from math import *
from datetime import timedelta
from datetime import datetime
from random import randint

#polygons imports
from scipy.spatial import Voronoi
import numpy as np
import matplotlib.pyplot as plt

#lines imports
from sets import Set
from itertools import tee, izip

def show_help():
	print './plp.py <type> <min lat> <min long> <max lat> <max long> <rows>'
	print './plp.py points 85.0 -179.0 -85.0 179.0 20'
	print 'Outputs: either POINT(...), LINESTRING(... , ...) or POLYGON ((... , ... , ...)) in CSV format'

def unique_rows(A, return_index=False, return_inverse=False):
	"""
	Similar to MATLAB's unique(A, 'rows'), this returns B, I, J
	where B is the unique rows of A and I and J satisfy
	A = B[J,:] and B = A[I,:]

	Returns I if return_index is True
	Returns J if return_inverse is True
	"""
	A = np.require(A, requirements='C')
	assert A.ndim == 2, "array must be 2-dim'l"

	B = np.unique(A.view([('', A.dtype)]*A.shape[1]),
			   return_index=return_index,
			   return_inverse=return_inverse)

	if return_index or return_inverse:
		return (B[0].view(A.dtype).reshape((-1, A.shape[1]), order='C'),) \
			+ B[1:]
	else:
		return B.view(A.dtype).reshape((-1, A.shape[1]), order='C')

def pairwise(iterable):
	a, b = tee(iterable)
	next(b, None)
	return izip(a, b)

def voronoi_finite_polygons_2d(vor, radius=None):
	"""
	Reconstruct infinite voronoi regions in a 2D diagram to finite
	regions.

	Parameters
	----------
	vor : Voronoi
		Input diagram
	radius : float, optional
		Distance to 'points at infinity'.

	Returns
	-------
	regions : list of tuples
		Indices of vertices in each revised Voronoi regions.
	vertices : list of tuples
		Coordinates for revised Voronoi vertices. Same as coordinates
		of input vertices, with 'points at infinity' appended to the
		end.

	"""

	if vor.points.shape[1] != 2:
		raise ValueError("Requires 2D input")

	new_regions = []
	new_vertices = vor.vertices.tolist()

	center = vor.points.mean(axis=0)
	if radius is None:
		radius = vor.points.ptp().max()*2

	# Construct a map containing all ridges for a given point
	all_ridges = {}
	for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
		all_ridges.setdefault(p1, []).append((p2, v1, v2))
		all_ridges.setdefault(p2, []).append((p1, v1, v2))

	# Reconstruct infinite regions
	for p1, region in enumerate(vor.point_region):
		vertices = vor.regions[region]

		if all(v >= 0 for v in vertices):
			# finite region
			new_regions.append(vertices)
			continue

		# reconstruct a non-finite region
		ridges = all_ridges[p1]
		new_region = [v for v in vertices if v >= 0]

		for p2, v1, v2 in ridges:
			if v2 < 0:
				v1, v2 = v2, v1
			if v1 >= 0:
				# finite ridge: already in the region
				continue

			# Compute the missing endpoint of an infinite ridge

			t = vor.points[p2] - vor.points[p1] # tangent
			t /= np.linalg.norm(t)
			n = np.array([-t[1], t[0]])  # normal

			midpoint = vor.points[[p1, p2]].mean(axis=0)
			direction = np.sign(np.dot(midpoint - center, n)) * n
			far_point = vor.vertices[v2] + direction * radius

			new_region.append(len(new_vertices))
			new_vertices.append(far_point.tolist())

		# sort region counterclockwise
		vs = np.asarray([new_vertices[v] for v in new_region])
		c = vs.mean(axis=0)
		angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
		new_region = np.array(new_region)[np.argsort(angles)]

		# finish
		new_regions.append(new_region.tolist())

	return new_regions, np.asarray(new_vertices)

def main(argv):
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

	type = sys.argv[1]
	minlat = float(sys.argv[2])
        minlong = float(sys.argv[3])
        maxlat = float(sys.argv[4])
        maxlong = float(sys.argv[5])
	rows = int(sys.argv[6])
	
	if( fabs(minlat) > 85.05113 or fabs(maxlat) > 85.05113 ):
		print "Lattitude not within acceptable range"
		sys.exit(0)
	if( fabs(minlong) > 179.999999999 or fabs(maxlong) > 179.999999999 ):
		print "Longtitude not within acceptable range"
		sys.exit(0)
	
	#radius = max([ fabs(minlat-maxlat), fabs(minlong-maxlong) ])/2
	radius = 0
	
	#header
	print "WKT"

	points = np.empty(shape=[0, 2])
		
	for num in range(0,rows):
		lat = random.uniform(minlat,maxlat)
		long = random.uniform(minlong,maxlong)
		points = np.append(points, [[lat, long]], axis=0)
		
		if( type == "points" ):
			#print "%s%s%s" % (lat,',',long)
			print "%s%s%s%s%s" % ( '"POINT (', lat, ' ',  long, ')"' )
	
	if( type == "polygons" ):
		vor = Voronoi(points)
		regions, vertices = voronoi_finite_polygons_2d(vor, radius=radius)
		
		#print vor.vertices
		#print vor.regions
		#print "======================="
		#print vertices
		#print regions
		#print "======================="
		
		for polygonvertexoffsets in regions:
			
			print '"POLYGON((',
			
			for vertexoffset in polygonvertexoffsets:
				vertex = vertices[vertexoffset]
				if( (min([minlat, maxlat]) <= vertex[0] <= max([minlat, maxlat])) and (min([minlong, maxlong]) <= vertex[1] <= max([minlong, maxlong])) ):
					print vertex[1], ' ', vertex[0], ',',
			
			#dont output comma after last coordinate
			vertexoffset = polygonvertexoffsets[0]
			vertex = vertices[vertexoffset]
			print vertex[1], ' ', vertex[0], '))"'

	if( type == "lines" ):
		vor = Voronoi(points)
                regions, vertices = voronoi_finite_polygons_2d(vor, radius=radius)
		lines = np.empty(shape=[0, 4])
		
		for polygonvertexoffsets in regions:
			for voffset1, voffset2 in pairwise(polygonvertexoffsets):
				vertex1 = vertices[voffset1]
				vertex2 = vertices[voffset2]
				lines = np.append(lines, [[vertex1[1], vertex1[0], vertex2[1], vertex2[0]]], axis=0)
		
		uniquelines = unique_rows(lines)
		for line in uniquelines:
			print '"LINESTRING(', line[0], line[1], ',', line[2], line[3], ')"'

if __name__ == "__main__":
	main(sys.argv[1:])
