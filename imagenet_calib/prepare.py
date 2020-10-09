"""
This python file is to prepare ImageNet calibration dataset.
It does two things:
    1. It randomly selects 300 images from source folder
    2. It copies the images in the img folder here, and writes out a list
       The list looks like this:
		n01440764_985.JPEG 0
		n01443537_9347.JPEG 0
		n01484850_8799.JPEG 0
"""

import os
import glob
from shutil import copy

source_dir = '/home/SharedDatasets/imagenet'

if __name__ == "__main__":
    
    dst_dir = os.path.join( os.getcwd(), 'img')
    if not os.path.exists(dst_dir): os.makedirs(dst_dir)    
    traverse_max = 300
    image_list = list()
    for i, file in enumerate(glob.iglob(source_dir + '/**/*.JPEG', recursive=True)):
        if i >= traverse_max : break
        filename = file.split(os.sep)[-1]
        dst_path = os.path.join(dst_dir, filename)
        image_list.append(filename + " 0 \n")
        print(f'copying file {file} to {dst_path}')
        copy(file, dst_path)
    
    list_file = "./imagenet_calib.txt"
    with open(list_file, 'w') as f:
        f.writelines(image_list)
        
