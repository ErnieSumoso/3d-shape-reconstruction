import random
# parámetros
category_name = "exp2"
category_code = "70309660"
category_total = 4590 # distribución 80-20 siempre
path_categories = "/data/esumoso/pmo/data/categories.txt"
path_lists = "/data/esumoso/pmo/data/lists"
# cálculos
test_total = int(round(category_total * 0.2, 0)) # 20%
train_total = category_total - test_total # 80%
# categories.txt - añadir categoría
file_categories = open(path_categories,"a")
file_categories.write(category_code + " " + category_name + "\n")
file_categories.close()
# all_test.list - añadir todos los objetos
file_alltest = open(path_lists + "/all_test.list","a")
for i in range(category_total):
	file_alltest.write(category_code + " " + str(i+1).zfill(4) + "\n") # 70309661 0001
file_alltest.close()
# definir conjuntos test y train
test_strs = [] # "0001","0004","0007"...
while len(test_strs) < test_total:
	random_number = str(random.randint(1, category_total)).zfill(4)
	if random_number not in test_strs:
		test_strs.append(random_number)
train_strs = [] # "0002","0003","0005","0006"...
for i in range(category_total):
	if str(i + 1).zfill(4) not in test_strs:
		train_strs.append(str(i + 1).zfill(4))
test_strs.sort()
train_strs.sort()
# _test.list y _train.list - crear archivos
file_test = open(path_lists + "/" + category_code + "_test.list","a")
file_train = open(path_lists + "/" + category_code + "_train.list","a")
for st in test_strs:
	file_test.write(st+"\n")
for st in train_strs:
	file_train.write(st+"\n")
file_test.close()
file_train.close()
# imprimir distribución
print("80% - " + str(len(test_strs)))
print("20% - " + str(len(train_strs)))