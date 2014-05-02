import cv
import cv2
import numpy as np
import Image


kernel = np.ones((8, 8), np.uint8)
kernel1 = np.ones((2, 2), np.uint8)
img = cv2.imread('LantingXu.jpg')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


ret,th1 = cv2.threshold(imgray, 64, 255, cv2.THRESH_BINARY)
th1 = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
th1 = cv2.morphologyEx(th1, cv2.MORPH_ERODE, kernel1)
ret,th1 = cv2.threshold(th1, 64, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(img, contours, -1, (255,255,255), -1)
#cv2.imshow('image', img)
#cv2.waitKey()


f = Image.open("LantingXu.jpg")
total = len(contours)

for h, cnt in enumerate(contours):
    print '%s' % (total - h)
    
    if len(cnt) > 100:
        # top_left & bottom_right
        x_list = []
        y_list = []
        for i in cnt:
            x_list.append(i[0][0])
            y_list.append(i[0][1])
        
        margin = 50
        x0 = min(x_list)-margin
        y0 = min(y_list)-margin
        x1 = max(x_list)+margin
        y1 = max(y_list)+margin

        print x0, y0, x1, y1
        seperated_area = f.crop((x0, y0, x1, y1))
        seperated_area.save('tmp/%s.jpg'%h)
        
        mask = np.zeros(imgray.shape, np.uint8)
        #mask = np.zeros(imgray.shape, np.uint8)
        cv2.drawContours(mask, [cnt], 0, 255, -1)
        mean = cv2.mean(img, mask=mask)
        cv2.imwrite('tmp/%s_mask.jpg'%h, mask)
    