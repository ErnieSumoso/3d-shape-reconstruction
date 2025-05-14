import glob, os
# parámetros
objects = ['0001','0002','0003','0004']
scales = ['0.005583','0.005583','0.004583','0.004383']
loops = 6
rot = "60.0"
path_shapenet = "/home/esumoso/ssr"
path_input = "/data/HuacosFinal/models"
path_output = "/home/esumoso/renderings"
input_folder = "models"
category_code = "70309660"

# crear carpeta output
os.chdir(path_output)
os.system("mkdir "+category_code)
external_counter = 0
# procesar cada objeto
for index_obj, obj in enumerate(objects):
	for i in range(loops):
		print(obj+" - "+str(i)) # imprimir avance
		external_counter += 1 # contador 1-4086
		str_external_counter = str(external_counter).zfill(4) # 0001
		os.chdir(path_shapenet)
		os.system("find "+path_input+" -name "+obj+".obj -print0 | xargs -0 -n1 -P3 -I {} blender --background --python render_blender.py -- --output_folder "+path_output+" {} --scale="+scales[index_obj]+" --loop="+str(i)+" --rot="+rot)
		# crear carpeta de la secuencia
		os.chdir(path_output + "/" + category_code)
		os.system("mkdir "+str_external_counter)
		os.chdir(path_output + "/" + input_folder)
		# mover archivos
		os.system("mv * "+path_output+ "/" +category_code+ "/" +str_external_counter)
		os.chdir(path_output+ "/" +category_code+ "/" +str_external_counter)
		# cambiar nombres de imágenes 0-71
		names = glob.glob("*.png")
		names.sort()
		for j, name in enumerate(names):
			os.system("mv "+name+" "+str(j)+".png")