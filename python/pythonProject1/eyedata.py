import os
from PIL import Image
import random
c = 0

path = f"C:\\Users\\Kiot\\Desktop\\eyes\\Closed"
files = os.listdir(path)

print(f"파일수: {len(files)}")

random.shuffle(files)

# for f, file in enumerate(files):
#
#     image = Image.open(path+"\\"+file)
#     image = image.convert("RGB")
#     resize_img = image.resize((86, 86))
#     resize_img.save(f"C:\\Users\\Kiot\\Desktop\\eyes\\Open\\_{c:0>5}.jpg", "JPEG")
#     c += 1
for f, file in enumerate(files):
    image = Image.open(path+"\\"+file)
    resize_img = image.resize((86, 86))
    for i in range(5):
        rotated_image = resize_img.rotate(i*90)
        rotated_image.save(f"C:\\Users\\Kiot\\Desktop\\eyes\\Closed1\\_{4*f+i:0>5}.jpg", "JPEG")
