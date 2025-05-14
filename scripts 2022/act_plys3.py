import numpy as np
import open3d as o3d
import os

category_code = "70309649"
total_objects = 962 # <= 9999
strs = [] # "0001" - "0962"
# creamos lista de strings
for i in range(total_objects):
	strs.append(str(i+1).zfill(4))
# procesar cada objeto
for st in strs:
	# copiamos archivo txt de malla
	os.system("cp "+st+".points.ply2.txt "+category_code+"/ply/"+st+".points.ply2.txt")
	# abrimos los 2 archivos de la malla
	file = open(st+".points.ply")
	fileply2 = open(st+".points.ply2.txt")
	# leemos el número de vértices de "file"
	for i in range(3): file.readline()
	num_vertex = file.readline().strip().split()[2]
	# movemos el puntero del archivo al 1° punto
	for i in range(9): file.readline()
	# leemos el centro del objeto y su escala de "fileply2"
	center = fileply2.readline().strip().split()
	scale = float(fileply2.readline().strip().split()[0])
	# creamos nuevo archivo ply
	os.chdir(category_code+"/ply")
	new_file = open(st+".points.ply","x")
	new_file.write("ply\n")
	new_file.write("format ascii 1.0\n")
	new_file.write("element vertex "+num_vertex+"\n")
	new_file.write("property float x\n")
	new_file.write("property float y\n")
	new_file.write("property float z\n")
	new_file.write("property float nx\n")
	new_file.write("property float ny\n")
	new_file.write("property float nz\n")
	new_file.write("element face 0\n")
	new_file.write("property list uchar int vertex_indices\n")
	new_file.write("end_header\n")
	# calculamos y escribimos los nuevos puntos en la nueva malla # nuevo punto = (punto anterior - centro) * escala
	for vertex in range(int(num_vertex)):
		point = file.readline().strip().split() # leer punto anterior
		new_point = [round((float(point[0])-float(center[0]))*scale,6),round((float(point[1])-float(center[1]))*scale,6),round((float(point[2])-float(center[2]))*scale,6)]
		new_file.write(str(new_point[0])+' '+str(new_point[1])+' '+str(new_point[2])+' '+point[3]+' '+point[4]+' '+point[5]+'\n')
	os.chdir("../..")
	file.close()
	fileply2.close()
	new_file.close()
	print("Creando PLY: "+st)
# generamos npy's a partir de los ply's recién creados
os.chdir(category_code)
for st in strs:
	os.chdir("ply")
	ply_load = o3d.io.read_point_cloud(st+".points.ply")
	npy_load = np.asarray(ply_load.points)
	print("Guardando NPY: "+st+" - "+str(npy_load.shape))
	os.chdir("..")
	np.save(st+".points.ply.npy",npy_load)