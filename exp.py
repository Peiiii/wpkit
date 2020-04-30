import wpkit.cv.transform.opencv as cvtrans
import cv2
from PIL import Image
# import imghdr

def show(img):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    Image.fromarray(img).show()
f=r'D:\work\wpkit\data\test\0.jpg'
img=cv2.imread(f)

show(img)
# img=gamma_trans(img,0.2)
# img=cvtrans.adjust_hue(img,20)
show(img)

