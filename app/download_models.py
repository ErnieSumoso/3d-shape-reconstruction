import gdown
import os

# Create models path if it doesnt exist yet
if not os.path.exists("models"):
    os.makedirs("models")
if not os.path.exists("models/high-capacity"):
    os.makedirs("models/high-capacity")
if not os.path.exists("models/low-capacity"):
    os.makedirs("models/low-capacity")

# Set Google Drive file ID (extracted from the URL) and path
models_dict = {'1nj8zjdBxX8LK2y4crZS9swEqv3R7UWTo':"models/high-capacity/02691156.keras",
               '1B94JXvj0MOUglWAvCIMwzPzeRXGE2vXj':"models/high-capacity/03001627.keras",
               '1AikyRTB1xmIDp2YYMdI5nC7gqjGfalP2':"models/high-capacity/03636649.keras",
               '19QJq-j-CDXTV4KmuGID3cl7MspdggjTo':"models/high-capacity/04090263.keras",
               '1KQj5ja_vI2WQvaU_1hcFDN55wtGqdKHt':"models/high-capacity/04256520.keras",
               '1iErOFND5kIoGOkxauIWZ5t_Plk8f3oNG':"models/high-capacity/04379243.keras",
               '1V9TBH1zz4HCJ48nJsgDt3MaTskEs_mq7':"models/low-capacity/02808440.keras",
               '1qiFb7ELbIvPjMlAmaCuapx62SSeG-hTU':"models/low-capacity/02828884.keras",
               '19sSfkOdv72neEQo0IDUVa0xGB6KC7ybx':"models/low-capacity/02924116.keras",
               '1K06r9eCHuJlY9LG8skyGiqKWRyBxXCLN':"models/low-capacity/02933112.keras",
               '15RxMY1f10pXKRiFc0Q5iZcBs3h6r7ITv':"models/low-capacity/02992529.keras",
               '1YPxvKQA59hT7RWhPQfh-u5FBk4rzSlc2':"models/low-capacity/03046257.keras",
               '16iaqwsuoicgT1jtYpIRBXZ2QURGkftux':"models/low-capacity/03211117.keras",
               '1MQK7iFk020OT6PcbEu2gJhbbqWfQc1EO':"models/low-capacity/03325088.keras",
               '1EPUT8eXwA58hljUeHoR7OaVXFrRnCRhr':"models/low-capacity/03467517.keras",
               '1B3KgiUR61Xa_LAzDks0dX6jo8SSdmpp9':"models/low-capacity/03691459.keras",
               '1RyRQSvm-MF-sJjTAdFHhfjz5QaC-QnAL':"models/low-capacity/04530566.keras",               
               }

for i, (id, path) in enumerate(models_dict.items()):
    # Download URL format for gdown
    url = f'https://drive.google.com/uc?id={id}'

    # Download the file
    gdown.download(url, path, quiet=False)