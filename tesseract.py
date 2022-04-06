from PIL import Image
import pytesseract
import numpy as np
import os

text=''
for filename in os.listdir(r'.\pics'):
    img = np.array(Image.open(rf".\pics\{filename}", mode='r'))

    img_data = pytesseract.image_to_string(img)
    text= text + '\n\n' + img_data

print(text.split())