import os
from exif import Image


mydir = r'd:/album/digikep/2024/2024iphone_06_teszt/'

files = [f for f in os.listdir(mydir) if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')]
if len(files) != 0:
    for f in files:
        with open(mydir+f, 'rb') as img_file:
            img = Image(img_file)

        # folder name will come from the file exif attribute datetime_original
        dateinfo = img.get('datetime_original')[:10]
        datedir = ''.join(dateinfo.split(':'))
        print(f'Picture {f} was taken on day {datedir}.')
        
        # create directory name
        picdir = rf'd:/album/digikep/{dateinfo[0:4]}/{datedir}/'
        #print(picdir)
        
        # create the picture directory except it already exists
        try:
            os.mkdir(picdir)
        except:
            pass
        
        # move the file to the picture directory
        try:
            os.rename(mydir+f, picdir+f)
        except:
            print(f'Relocation of {mydir+f} failed.')
        
else:
    print(f'{mydir} folder doesn\'t contain any jpg file.')

