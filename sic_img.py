import this

import cv2,os
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image

window_name = None


# 加載CSV文件的函數
def btn_save_file():
    global gthreshold
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("PNG file", "*.png"),("All Files", "*.*") ))
    if file:
        im2 = Image.fromarray(cv2.cvtColor(gthreshold, cv2.IMREAD_GRAYSCALE))
        im2.save(file.name)
    return file



# Set up mouse callback
def update_for_save(event, x, y, flags, params):
    global gray, window_name

    # On left mouse button down (i.e. when the focus goes to the window), update global variables
    if event == cv2.EVENT_LBUTTONDOWN:
        gray = params[1]
        window_name = params[0]
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:
            file = btn_save_file()
            #print('Clicked on Button!--> ', file.name)
            return file.name

# 定義調整亮度對比的函式
def adjust(i, c, b):
    global window_name
    print("----------1------------> ",type(i),i.size,i.shape,i,c, b)
    output = i * (c/100 +1) - c + b    # 轉換公式
    output = np.clip(output, 0, 255)
    output = np.uint8(output)
    cv2.imshow(window_name , output)

# 定義調整threshold的函式
def adjust1(i,a):
    global gthreshold,window_name
    print("----------2------------> ",type(i),i.size,i.shape,i,a)
    output = i * (a+ 1) -a     # 轉換公式
    output = np.clip(output, 0, 255)
    output = np.uint8(output)
    cv2.imshow(window_name , output)
    #cv2.imwrite("/home/k900/Downloads/DIC-demo-master/test51.png",output)
    gthreshold = output

# 定義調整亮度函式
def brightness_fn(val):
    global gray,output1,output4, contrast, brightness,threshold , window_name
    brightness = val - 0
    keydict={"gray":gray}#,"gray1":gray1,"gray2":gray2,"gray3":gray3,"gray4":gray4,"gray5":gray5}
    adjust(keydict[window_name], contrast, brightness)


# 定義調整對比度函式
def contrast_fn(val):
    global gray,output1, output4 ,contrast, brightness,threshold   , window_name
    contrast = val - 0
    keydict={"gray":gray}#,"gray1":gray1,"gray2":gray2,"gray3":gray3,"gray4":gray4,"gray5":gray5}
    adjust(keydict[window_name], contrast, brightness)


# 定義調整threshold函式
def threshold_fn(val):
    global gray,output1, output4 ,contrast, brightness,threshold   , window_name
    threshold = val - 0
    keydict={"gray":gray}#,"gray1":gray1,"gray2":gray2,"gray3":gray3,"gray4":gray4,"gray5":gray5}
    adjust1(keydict[window_name], threshold)


if __name__ == '__main__':
    global gray, output1, output2, output3, output4, output5
    all_img = glob('/media/k900/SP UFD U3/KOH_SiC_121124/single_new_afterKOH/3_7_0d.bmp')#/home/k900/Documents/wind-turbine-project/20240729/CREE_0322_141.png')
    dd =  "/20240729/output10_threshold_24/"
    cur_dir = os.getcwd()
    img_save = False#True
    img_show = True#False
    thresVal = 24
    window_name = None
    # button dimensions (y1,y2,x1,x2)
    button = [5,30,5,75]

    if (os.path.exists(cur_dir+ dd) == False):
        os.makedirs(cur_dir+ dd)
    cur_dir1 = cur_dir + dd

    for oimg in all_img:
        #print("-------->: ", oimg)
        oimg1 = oimg.split("/")[-1:][0]

        gray = cv2.imread(oimg,cv2.IMREAD_GRAYSCALE)#/home/k900/Pictures/123.png')
        #ret, gray1 = cv2.threshold(gray, thresVal, 255, cv2.THRESH_BINARY_INV)
        # gray2 = cv2.adaptiveThreshold(gray, thresVal, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        # gray3 = cv2.adaptiveThreshold(gray, thresVal, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        # gray4 = cv2.adaptiveThreshold(gray, thresVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # gray5 = cv2.adaptiveThreshold(gray, thresVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)


        tmp1 = ["gray"]#,"gray1","gray2","gray3","gray4","gray5"]
        tmp2 = [gray]#, gray1, gray2, gray3, gray4, gray5]
        for idx in range(len(tmp1)):
            cv2.namedWindow(tmp1[idx],  cv2.WINDOW_NORMAL| cv2.WINDOW_KEEPRATIO)
            cv2.setMouseCallback(tmp1[idx], update_for_save, [tmp1[idx], tmp2[idx]])
            #cv2.setMouseCallback('gray', update_for_save, ['gray', gray])
            # add cv2 image page button & button-text
            tmp2[idx][button[0]:button[1], button[2]:button[3]] = 255
            cv2.putText(tmp2[idx], 'Save', (5, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0), 2)

        if img_show == True:
            for idx in range(len(tmp1)):
                cv2.imshow(tmp1[idx], tmp2[idx])
                #cv2.imshow('gray',  gray)

        if img_save == True:
            cv2.imwrite(cur_dir1 + oimg1.split(".")[0]+'_gray.png', gray)
            # cv2.imwrite(cur_dir1 + oimg1.split(".")[0]+'_output1.png', gray1)
            # cv2.imwrite(cur_dir1 + oimg1.split(".")[0]+'_output4.png', gray4)

        contrast = 0  # 初始化要調整對比度的數值
        brightness = 0  # 初始化要調整亮度的數值
        threshold = 0 # 初始化要調整threshold的數值

        for idx in tmp1 :
            cv2.createTrackbar('brightness', idx, 0, 255, brightness_fn)  # 加入亮度調整滑桿
            cv2.setTrackbarPos('brightness', idx, 0)
            cv2.createTrackbar('contrast', idx, 0, 255, contrast_fn)      # 加入對比度調整滑桿
            cv2.setTrackbarPos('contrast', idx, 0)
            cv2.createTrackbar('threshold', idx, 0, 255, threshold_fn)      # 加入threshold調整滑桿
            cv2.setTrackbarPos('threshold', idx, 0)

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        plt.figure()
        plt.title("Grayscale Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")
        plt.plot(hist)
        plt.xlim([0, 256])

        if img_save == True:
            plt.savefig(cur_dir1 +oimg1.split(".")[0]+"_hist.png")#, pad_inches=0, bbox_inches='tight', dpi=600)
    if img_show == True:
        plt.show()
        keycode = cv2.waitKey(0)
        if keycode & 0xFF == ord('q'):
            cv2.destroyAllWindows()
