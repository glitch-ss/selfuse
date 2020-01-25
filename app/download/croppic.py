import os
import colorsys
from PIL import Image, ImageDraw, ImageFile
import re
ImageFile.LOAD_TRUNCATED_IMAGES = True

def crop(image,new_file):
    w_new=image.size[0]
    h_new=image.size[1]
    lowest=h_new
    print h_new
    image.thumbnail((w_new,h_new))
    for i in range(0,w_new-1):
        for j in range(0,h_new-1):
            x,y,z=image.getpixel((i,j))
            if x <250 and y < 250 and z<250:
                if j < lowest:
                    lowest=j
    print lowest
    if lowest<h_new/4:
        print 'no new pic'
        return 0
    white=int((h_new-lowest)/7*3)
    h_start=lowest-white
    img=image.crop((0,h_start,w_new,h_new))
    img.save(new_file,'jpeg')



Path=os.path.abspath('.')
handbags_file=os.path.join(Path,'handbags')
newhandbags_file=os.path.join(Path,'newhandbags')
if not os.path.exists(newhandbags_file):
    os.mkdir(str(newhandbags_file))
bags=os.listdir(handbags_file)
for bag in bags:
    print bag
    bag_file=os.path.join(handbags_file,bag)
    new_bag_file=os.path.join(newhandbags_file,bag)
    if not os.path.exists(str(new_bag_file)):
        os.mkdir(str(new_bag_file))
    pics=os.listdir(bag_file)
    for pic in pics:
        if not pic.endswith('jpeg'):
            continue
        pic_file=os.path.join(bag_file,pic)
        new_name=os.path.join(new_bag_file,pic)
        image=Image.open(pic_file)
        w=image.size[0]
        h=image.size[1]
        w_new=int(w*0.25)
        h_new=int(h*0.25)
        image.thumbnail((w_new,h_new))
        image.save(new_name)
        if '+1.' in pic:
            crop(image,new_name)
        image.close()
  
