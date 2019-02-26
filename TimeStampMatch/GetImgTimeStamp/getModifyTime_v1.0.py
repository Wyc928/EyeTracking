# -*- coding: utf-8 -*-
'''
    Author: WangYongchen
    Date: 2/25/2019
    Version: 1.0

    Function:
    v1.0: 
    read the modify time of pictures and save them in a textfile
    
    Instruction:
    Put this py script into the pictures' folder and the result text file will generate in it.
'''
import os
import time

'''
    Convert the time stamp to date-time formation
'''

def TimeStampToTime(time_stamp):
    #print(time_stamp)
    time_struct = time.localtime(time_stamp)
    data_head = time.strftime('%Y-%m-%d %H:%M:%S',time_struct)
    str_time = str(time_stamp)
    start = str_time.find('.')+1
    end = str_time.find('.')+4
    data_milisecs = str_time[start:end]
    #print(data_milisecs)
    mili_time_stamp = "%s %s" % (data_head, data_milisecs)
    return mili_time_stamp

'''
    Get the modify time of a file 
'''
def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

'''
    Extract all image files from file list and sort for the right order
'''
def get_SortedImageFiles(file_list):
    image_list = []
    for img in file_list:
            img_head = img.split('.')[0]
            if img_head.isdigit() == False:
                continue
            image_list.append(img)
            
    # sort for the right order of images
    image_list.sort(key = lambda x:int(x[0:-4]))
    return image_list

'''
    main function
'''

def main():
        '''
        ModifyTime.txt is the output file
        '''
        output_file_name = 'ModifyTime.txt'
        print(output_file_name)
        mt_file = open(output_file_name,'w+')
        dir_name = os.getcwd()
        file_list = os.listdir(dir_name)

        '''
        extract all image files from file list
        '''
        image_list = get_SortedImageFiles(file_list)        
        
        
        '''
        list all images and do loop for modify time
        '''
        count = 0
        
        for image_name in image_list:
                modify_time = get_FileModifyTime(image_name)
                mt_file.write("%d--%s--%s\r\n" % (count,modify_time,image_name))
                count = count + 1
                #if count > 5:
                #        break
        mt_file.close()
        
if __name__=='__main__':
        main()
