import imageio
import numpy as np
import os

# definimos paths
list_path = "/data/esumoso/pmo/data/lists/indoor_test.list"
backgrounds_path = "/data/esumoso/pmo/data/background"
rendering_path = "/data/esumoso/pmo/data/rendering"
sequences_path = "/data/esumoso/pmo/data/sequences" # donde se guardará el NPY (necesrio para generar malla)
created_path = "/home/esumoso/sequences" # donde se guardarán los PNG's (innecesarios para generar malla)
category_code = "70309660"
# definimos arreglo de objetos de los cuales se construirán secuencias
objects = [
'0013','0019','0031','0079',
'0139','0163','0169','0175',
'0193','0253','0259','0337',
'0343','0355','0391','0409',
'0421','0433','0463','0499',
'0529','1105','1543','2143'
]
# crear carpeta de categoría en rendering pmo
os.chdir(rendering_path)
os.system("mkdir " + category_code)
os.chdir(created_path)
os.system("mkdir " + category_code)
# guardamos nombres de los backgrounds
backgrounds_names = []
backgrounds_list = open(list_path)
for line in backgrounds_list:
	backgrounds_names.append(line.strip().split())
backgrounds_list.close()
# construimos la secuencia de cada objeto
for obj in objects:
	sequence = []
	# escogemos un background aleatorio
	index_background = np.random.randint(0, len(backgrounds_names))
	# creamos una carpeta para guardar los PNG's de la secuencia
	os.chdir(created_path + "/" + category_code)
	os.system("mkdir " + obj)
	os.chdir(obj)
	# construimos la secuencia del objeto
	for index_image in range(72):
		# recuperamos la imagen de renderings (sin fondo)
		image_rendering = imageio.imread(rendering_path + "/" + category_code + "/" + obj + "/" + str(index_image) + ".png")/255.0
		alpha = image_rendering[...,-1:]
		# recuperamos el background (solo fondo)
		image_background = imageio.imread(backgrounds_path + "/" + backgrounds_names[index_background][1] + "/" + str(index_image) + ".png")/255.0
		# combinamos ambas imágenes en una sola
		image_composite = image_rendering[...,:3] * alpha + image_background * (1 - alpha)
		imageio.imwrite(str(index_image) + ".png", image_composite)
		sequence.append(image_composite)
	# transformamos el arreglo en un uint8,con rangos 0-255 y 4° valor = 0
	final_sequence = np.zeros((72, 224, 224, 4), dtype=np.uint8)
	for idxI, i in enumerate(final_sequence):
		for idxJ, j in enumerate(i):
			for idxK, k in enumerate(j):
				final_sequence[idxI][idxJ][idxK] = np.array([round(sequence[idxI][idxJ][idxK][0]*255),round(sequence[idxI][idxJ][idxK][1]*255),round(sequence[idxI][idxJ][idxK][2]*255),0], dtype=np.uint8)
	# generamos el NPY a partir de la secuencia
	os.chdir(sequences_path + "/" + category_code)
	np.save(obj + ".npy", final_sequence)
	# imprimimos progreso
	print("Secuencia creada: " + obj)