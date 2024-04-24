from exif import Image

with open('IMG_1494.jpg', 'rb') as img_file:
    img = Image(img_file)

# folder name from the file exif attributte datetime_original
print(''.join(img.get('datetime_original')[:10].split(':')))