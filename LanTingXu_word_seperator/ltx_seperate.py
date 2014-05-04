import cv
import cv2
import numpy as np
import Image
import ImageDraw


kernel = np.ones((8, 8), np.uint8)
kernel1 = np.ones((2, 2), np.uint8)
img = cv2.imread('LantingXu.jpg')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


ret,th1 = cv2.threshold(imgray, 64, 255, cv2.THRESH_BINARY)
th1 = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
th1 = cv2.morphologyEx(th1, cv2.MORPH_ERODE, kernel1)
ret,th1 = cv2.threshold(th1, 64, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, 
                                       cv2.CHAIN_APPROX_SIMPLE)


f = Image.open("LantingXu.jpg")
total = len(contours)
draw = ImageDraw.Draw(f)

for h, cnt in enumerate(contours): 
    if len(cnt) > 100:
        print '%s:\t' % (total - h),
        # top_left & bottom_right
        x_list = []
        y_list = []
        for i in cnt:
            x_list.append(i[0][0])
            y_list.append(i[0][1])
        
        margin = 50
        x0 = min(x_list)
        y0 = min(y_list)
        x1 = max(x_list)
        y1 = max(y_list)
        print x0, y0, x1, y1
        
        draw.rectangle((x0, y0, x1, y1))
        #draw.line(((x0+x1)/2, y0, (x0+x1)/2, y1), 
        #          fill=(255,255,255), width=1)
        #draw.line(((x0,(y0+y1)/2, x1,(y0+y1)/2)), 
        #          fill=(255,255,255), width=1)
        
        seperated_area = f.crop((x0-margin, y0-margin, 
                                 x1+margin, y1+margin))
        seperated_area.save('tmp/%s.jpg'%h)
        
f.save('allinone.jpg')