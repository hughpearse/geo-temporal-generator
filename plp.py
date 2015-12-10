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
	print './plp.py <min lat> <min long> <max lat> <max long> <rows> <type>'
	print './plp.py 53.438528 -6.403656 53.196751 -6.099472 20 points'
	print 'Outputs: either POINT(...), LineString(... , ...) or POLYGON ((... , ... , ...)) in CSV format'

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
	
	minlat = float(sys.argv[1])
        minlong = float(sys.argv[2])
        maxlat = float(sys.argv[3])
        maxlong = float(sys.argv[4])
	rows = int(sys.argv[5])
	type = sys.argv[6]
	
	if( fabs(minlat) > 85.05113 or fabs(maxlat) > 85.05113 ):
		print "Lattitude not within acceptable range"
		sys.exit(0)
	if( fabs(minlong) > 179.999999999 or fabs(maxlong) > 179.999999999 ):
		print "Longtitude not within acceptable range"
		sys.exit(0)
	
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
		regions, vertices = voronoi_finite_polygons_2d(vor)
		
		for polygonvertexoffsets in regions:
			#print polygonvertexoffsets
			print '"POLYGON((',
			
			for vertexoffset in polygonvertexoffsets[:-1]:
				vertex = vertices[vertexoffset]
				print vertex[0],
				print ' ',
				print vertex[1],
				print ',',
			#dont place output after last coordinate
			vertexoffset = polygonvertexoffsets[-1]
			print vertex[0],
			print ' ',
			print vertex[1],
			print '))"'

	if( type == "lines" ):
		vor = Voronoi(points)
                regions, vertices = voronoi_finite_polygons_2d(vor)
		lines = np.empty(shape=[0, 4])
		
		for polygonvertexoffsets in regions:
			for voffset1, voffset2 in pairwise(polygonvertexoffsets):
				vertex1 = vertices[voffset1]
				vertex2 = vertices[voffset2]
				#aline =  (vertex1,vertex2)
				lines = np.append(lines, [[vertex1[0], vertex1[1], vertex2[0], vertex2[1]]], axis=0)
		
		uniquelines = unique_rows(lines)
		for line in uniquelines:
			print '"LINESTRING(',
			print line[0], line[1], ',', line[2], line[3],
			print ')"'

if __name__ == "__main__":
	main(sys.argv[1:])