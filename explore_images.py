import cv2
import numpy as np
from matplotlib import pyplot as plt

# file0 = 'E:/ACIL stuff/PICAM/image_date_2020_10_19_time_21_1_count_1_CamA.png'
file0 = 'E:/ACIL stuff/PICAM/image_date_2020_10_19_time_21_1_count_1_CamB.png'
img = cv2.imread(file0)
color = ('b','g','r')
plt.figure()
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()