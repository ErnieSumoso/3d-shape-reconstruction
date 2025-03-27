MODELS_BASE_PATH = "models"
IMAGE_URL = "https://raw.githubusercontent.com/ErnieSumoso/ErnieSumoso/refs/heads/main/website-background.jpg"
MODEL_NAME_DICT = {'bathtub': '02808440',
'bench': '02828884',
'bus': '02924116',
'cabinet': '02933112',
'phone': '02992529',
'clock': '03046257',
'display': '03211117',
'faucet': '03325088',
'guitar': '03467517',
'loudspeaker': '03691459',
'watercraft': '04530566',
'airplane': '02691156',
'chair': '03001627',
'lamp': '03636649',
'rifle': '04090263',
'sofa': '04256520',
'table': '04379243'}
LOW_CAPACITY_LABELS = [name + " - low capacity model (12.6 MB)" for name in list(MODEL_NAME_DICT.keys())[:-6]]
HIGH_CAPACITY_LABELS = [name + " - high capacity model (6.3 GB)" for name in list(MODEL_NAME_DICT.keys())[-6:]]
VOXEL_PREDICTION_THRESH = 0.5
VERTEX_OFFSETS = [(0, 0, 0),
(1, 0, 0),
(1, 1, 0),
(0, 1, 0),
(0, 0, 1),
(1, 0, 1),
(1, 1, 1),
(0, 1, 1)]
FACE_OFFSETS = [
(0, 1, 2, 3), # bottom
(4, 5, 6, 7), # top
(0, 1, 5, 4), # front
(2, 3, 7, 6), # back
(1, 2, 6, 5), # right
(3, 0, 4, 7)]  # left