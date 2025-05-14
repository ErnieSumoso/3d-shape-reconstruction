import os, imageio, subprocess, math
import numpy as np
# Definimos el pipeline como un procedimiento el cual recibe:
# filename = nombre del archivo video a procesar
# category = nombre de la categoría de piezas arqueológicas a la que pertenece el objeto
def process_mesh(filename, category):
	# Definir rutas a los diferentes archivos y carpetas que usaremos
	upload_path = "/data/esumoso/uploads"
	sequences_path = "/data/esumoso/pmo/data/sequences"
	alltest_path = "/data/esumoso/pmo/data/lists/all_test.list"
	pmo_path = "/data/esumoso/pmo"
	# Conseguir la extensión del video
	extension = get_file_extension(filename)
	name = get_file_name_only(filename)
	category_code = get_category_code(category)
	category_group = get_category_group(category)
	os.chdir(upload_path)
	# Aseguramos las extensiones de archivo permitidas: MP4, AVI
	if extension not in ["mp4","avi"]:
		return "Video extension not supported for "+filename+", try MP4 or AVI only."
	# Aseguramos el rango de fotogramas permitido: [72, 9999]
	total_frames = int(subprocess.check_output("ffmpeg -i "+new_filename+" -vcodec copy -f rawvideo -y /dev/null 2>&1 | tr ^M '\n' | awk '/^frame=/ {print $2}'|tail -n 1", shell=True))
	if total_frames < 72 or total_frames > 9999:
		return "Total frames out of range for "+filename+", try at least 72 frames (2.4s at 30 frames/second) and less than 10'000 frames (5min 33s)."
	# Aseguramos la existencia de la categoría seleccionada
	if category_code == "":
		return "Unknown category for "+filename+", try chosing one of the allowed categories."
	# Escalar el video a 224 x 224 pixeles
	os.system("ffmpeg -i "+filename+" -vf scale=224:224 "+name+"_224x224."+extension)
	new_name = name + "_224x224"
	new_filename = name + "_224x224" + "." + extension
	os.system("rm "+filename) # Borramos el video original
	# Generar fotogramas
	os.system("mkdir "+new_name)
	os.system("mv "+new_filename+" "+upload_path+"/"+new_name+"/"+new_filename)
	os.chdir(new_name)
	os.system("ffmpeg -i "+new_filename+" frame-%04d.png")
	os.system("rm "+new_filename) # Borramos el video escalado
	# Selección de 72 fotogramas
	increment = math.floor(total_frames / 72)
	frame_names = []
	for i in range(72):
		frame_names.append(str(int(i*step+1)).zfill(4))
	# Guardar imágenes seleccionadas como arreglo NumPy
	frames = []
	for name in frame_names:
		frame = imageio.imread(upload_path+"/"+new_name+"/frame-"+name+".png")
		frames.append(frame)
	# Procesar valores RGB del arreglo
	new_frames = np.zeros((72, 224, 224, 4), dtype=np.uint8)
	for idxI, i in enumerate(new_frames):
		for idxJ, j in enumerate(i):
			for idxK, k in enumerate(j):
				new_frames[idxI][idxJ][idxK] = np.array([round(frames[idxI][idxJ][idxK][0]*255),round(frames[idxI][idxJ][idxK][1]*255),round(frames[idxI][idxJ][idxK][2]*255),0], dtype=np.uint8)
	# Guardar arreglo como archivo NPY
	os.chdir(upload_path)
	os.system("rm -r "+new_name) # Borramos los fotogramas generados
	np.save(name+".npy", new_frames)
	os.system("mv "+name+".npy "+sequences_path+"/"+category_code+"/"+name+".npy")
	# Escribir la secuencia en el archivo del PMO: all_test.list
	alltest_file = open(alltest_path,"a")
	alltest_file.write(category_code+" "+name+"\n")
	alltest_file.close()
	# Procesar el archivo NPY
	os.chdir(pmo_path)
	os.system("model=checkpoint/"+category_group+"/"+category_code+"_pretrain_seed0/ep500.npz")
	os.system("python3 main.py --load=${model} --code=5e-2 --scale=2e-2 --lr-pmo=3e-3 --noise=0.1 --filecategory "+category_code+" --filename "+name+" --gpu 1;")	
	return "Succesfully generated mesh for "+filename+": "+category_code+"_"+name+".ply'"