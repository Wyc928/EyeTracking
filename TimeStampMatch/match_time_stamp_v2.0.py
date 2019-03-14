# -*- coding: utf-8 -*-
'''
    Author: WangYongchen
    Date: 3/3/2019
    Version: 2.0

    Previous Script:mapImg2Gaze_v1.0.py
    
    Function:
    map image files to gaze data and display, then generate .npz

    v2.0 add:
    match ball points to img file for visualization and confirmation of match results
    
    Instruction:
    check the right directory of image and gaze data and ball points file
'''
import os
import time
import sys
import numpy as np
import cv2 as cv

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
    Get the create time of a file 
'''
def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return t

'''
    main function
'''
root_folder = 'F:\\DataSet\\' + sys.argv[1]
save_gaze2img_name = root_folder + '\\GazeData\\match_gaze2img.txt'
save_ball2img_name = root_folder + '\\Ball\\match_ball2img.txt'
img_folder = root_folder + '\\IMAGE\\'

# 0:run main() function ; 1 (default): only run visualization
run_mode = '1' 

def main():
        # Warning
        print('################################################################')
        print('# WARNING: The Code Should Be Tested On A Small Dataset First! #')
        print('################################################################')

        '''
        Check the right directory of image and gaze data file
        '''
        gaze_file = root_folder + '\\GazeData\\GazeOriginalData.txt'
        ball_file = root_folder + '\\Ball\\BallOriginalPoints.txt'
        
        
                        
        npz_file = root_folder + '\\Img_Gaze_Package'
        
        #'data_LSC-eye-tracker_test.npz'
        save_gaze2img_file = open(save_gaze2img_name,'w+')
        
        file_list = os.listdir(img_folder)

        '''
           # extract all image files from file list
        '''
        image_list = get_SortedImageFiles(file_list)
        data_size = len(image_list)
        print("data size = %d" % (data_size))
        gaze = np.zeros([data_size, 2],dtype=float)
        ball = np.zeros([data_size, 2],dtype=float)
        # map img to gazedata by time stamp
        # if a match is obtained, gaze data will be recorded in save_gaze2img_file,
        # and the unmatched old gazedata above this pair will be removed

        '''
           # match gazedata to img files
        '''
        count = 0
        current_line_index = 0
        for image_name in image_list:
                image_directory = img_folder + image_name
                create_time = ("%.3f" % get_FileCreateTime(image_directory))

                #### For debug
                '''
                   # inner_cnt = 0
                '''
                with open(gaze_file,'r') as gaze_points:
                        #set read line_index
                        gaze_points.seek(current_line_index, 0)
                        next_line = gaze_points.readline()
                        
                        # nearest_data is the last result for gazedata match a image file
                        nearest_data = next_line.split('\t') # use timestamp as a big gap
                        nearest_data = nearest_data[1:4]
                        nearest_data[2] = float(nearest_data[2][0:-1]) # remove '\n' and convert to float
                        
                        while next_line:
                                vector = next_line.split('\t')
                                gazepoint_x = int(vector[1])
                                gazepoint_y = int(vector[2])
                                gaze_time_stamp = vector[3]
                                # remove '\n' in gaze_time_stamp
                                gaze_time_stamp = float(gaze_time_stamp[0:-1])
                                #if gap decrease, replace nearest_data. Else, break
                                gap = abs(float(gaze_time_stamp) - float(create_time))*1000
                                if gap < 1000: # ignore useless data in the beginning
                                    if gap < nearest_data[2]:
                                        nearest_data = [gazepoint_x, gazepoint_y, gap]
                                        print('%s\t%s\t%.3f\t%.3f\n' % (image_name,create_time,gaze_time_stamp,gap))
                                        current_line_index =  gaze_points.tell() # because the next line need to match in next circulation
                                    else:
                                        break;
                                next_line = gaze_points.readline()
                                #### For debug
                                '''
                                   # inner_cnt=inner_cnt + 1
                                   # if inner_cnt>20:
                                   #     break
                                '''
                        save_gaze2img_file.write("%s\t%s\t%s\n" % (nearest_data[0], nearest_data[1], nearest_data[2]))
                        # <list>gaze will be used when generate npz package
                        gaze[count] = nearest_data[0:2]
                        
                count = count + 1
                #### For debug
                
                #if count > 5:
                #        break
                
        save_gaze2img_file.close()

        print('\n# MATCH GAZE TO IMG FINISHED #\n')

        cv.waitKey(2000)

        '''
           match ballpoints to img files
           ONLY be used in visualization
        '''
        save_ball2img_file = open(save_ball2img_name,'w+')
        count = 0
        current_line_index = 0
        for image_name in image_list:
                image_directory = img_folder + image_name
                create_time = ("%.3f" % get_FileCreateTime(image_directory))

                #### For debug
                '''
                inner_cnt = 0
                '''
                current_line_index = 0
                with open(ball_file,'r') as ball_points:
                        #set read line_index
                        ball_points.seek(current_line_index, 0)
                        next_line = ball_points.readline()
                        
                        # nearest_data is the last result for balldata match a image file
                        nearest_data = next_line.split('\t') # use timestamp as a big gap
                        nearest_data[2] = float(nearest_data[2][0:-1]) # remove '\n' and convert to float
                        '''
                           match balldata to img files
                        '''
                        while next_line:
                                vector = next_line.split('\t')
                                ballpoint_x = int(vector[0])
                                ballpoint_y = int(vector[1])
                                ball_time_stamp = vector[2]
                                # remove '\n' in ball_time_stamp
                                ball_time_stamp = float(ball_time_stamp[0:-1])
                                #if gap decrease, replace nearest_data. Else, break
                                gap = abs(float(ball_time_stamp) - float(create_time)*1000)
                                if gap < 1000: # ignore useless data in the beginning
                                    if gap < nearest_data[2]:
                                        nearest_data = [ballpoint_x, ballpoint_y, gap]
                                        print('%s\t%s\t%f\t%f\n' % (image_name,create_time,ball_time_stamp,gap))
                                        current_line_index =  ball_points.tell() # because the next line need to match in next circulation
                                    else:
                                        break;
                                next_line = ball_points.readline()
                                #### For debug
                                '''
                                inner_cnt=inner_cnt + 1
                                if inner_cnt>20:
                                        break
                                '''
                        save_ball2img_file.write("%s\t%s\t%s\n" % (nearest_data[0],nearest_data[1], nearest_data[2]))

                count = count + 1
                #### For debug
                
                #if count > 5:
                #        break
                
        save_ball2img_file.close()

        '''
           Compress img and gazedata into npz package
        '''
        
        matched_gaze_data = np.loadtxt(save_gaze2img_name)
        width = 1600
        height = 900

        gaze_origin = gaze.copy()
        # save_gaze2img_name = 'match_gaze2img.txt'
        save_gaze2img_file = open(save_gaze2img_name,'r')
        faceData = np.zeros([data_size, 224, 224, 3],dtype=float)
        eyeTrackData = np.zeros([data_size, 2],dtype=float)
        for i in range(data_size):
            fileName = '%s%d.bmp' % (img_folder, i)
            print('Preprocessing : %s' % (fileName))
            imageSrc = cv.imread(fileName)
            image = cv.resize(imageSrc, (224, 224))
            faceData[i, :, :, :] = image
            gaze[i, 0] = gaze[i, 0] / width
            gaze[i, 1] = gaze[i, 1] / height
            # print(gaze[i])
            eyeTrackData[i, :] = gaze[i, :]
            
            ### For debug
            #if i > 5:
            #    break
        print('Saving Data. Please wait.')
        np.savez_compressed(npz_file,faceData=faceData,eyeTrackData=eyeTrackData)
        print('Save Finished.')
        
        # show the matching result
        visual()
        
#def useless_func():
        
    
'''
    only for visualization
'''
def visual():
    #root_folder = 'F:\\DataSet\\' + sys.argv[1] + '\\'
    img_folder = root_folder + '\\IMAGE\\'
    gaze_file = save_gaze2img_name
    ball_file = save_ball2img_name
    file_list = os.listdir(img_folder)
    width = 1280
    height = 720
    waitTime = int(sys.argv[2])
    if waitTime < 200:
        waitTime = 200
    
    '''
        extract all image files from file list
    '''
    image_list = get_SortedImageFiles(file_list)
    data_size = len(image_list)
    with open(gaze_file,'r') as gaze_data:
      with open(ball_file,'r') as ball_data:
        # directory
        gaze_data_list = gaze_data.readlines()
        ball_data_list = ball_data.readlines()
        count = 0
        for gaze_data,ball_point in zip(gaze_data_list,ball_data_list):
            
            gaze_vector = gaze_data
            gaze_vector = gaze_vector.split('\t')
            
            if(gaze_vector[0]=='\n'):
                continue
            
            gaze_point_x = int(gaze_vector[0])
            gaze_point_y = int(gaze_vector[1])

            ball_vector = ball_point
            ball_vector = ball_point.split('\t')
            
            ball_point_x = int(ball_vector[0])
            ball_point_y = int(ball_vector[1])
            
            fileName = '%s%d.bmp' % (img_folder, count)
            imageSrc = cv.imread(fileName)
            ###image = cv.resize(imageSrc, (width,height))
            # attention : mirror process
            # gaze point
            cv.circle(imageSrc, (width - gaze_point_x, gaze_point_y), 10, (0,0,255), 3)
            # ball point
            cv.circle(imageSrc, (width - ball_point_x, ball_point_y), 10, (255,255,0), 3)
            image = cv.resize(imageSrc, (width,height))
            # show img name at the leftdown conner
            fontFace = cv.FONT_HERSHEY_DUPLEX
            fontScale = 1
            fontcolor = (0, 255, 255) # BGR
            thickness = 1 
            lineType = 4
            cv.putText(image, fileName, (40,700), fontFace, fontScale, fontcolor,thickness,lineType)
            #show gaze-data and ball-point
            cv.putText(image, '%d   %d'%(gaze_point_x,gaze_point_y), (40,50), fontFace, fontScale, fontcolor,thickness,lineType)
            cv.putText(image, '%d   %d'%(ball_point_x,ball_point_y), (40,100), fontFace, fontScale, fontcolor,thickness,lineType)
            cv.imshow('preview',image)

            if cv.waitKey(waitTime) == 27:
                break
            count = count + 1
            ### For debug
            #if count > 5 :
            #    break
            
if __name__=='__main__':
    # sys.argv :
    if len(sys.argv) == 4:
        run_mode = sys.argv[3]
    if run_mode == '0':
        print('RUN_MODE_0:Main function will start in 2 seconds.')
        cv.waitKey(2000)
        main()
    else:
        print('RUN_MODE_1:Visualization will start in 2 seconds.')
        cv.waitKey(2000)
        visual()
