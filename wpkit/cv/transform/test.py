from wpkit.cv.transform.cv2 import gamma_trans
import cv2
from PIL import Image
def show(img):
    Image.fromarray(img).show()
f=r'E:\datasets\chaoyuan\raw_data\超远数据20200108\0198\_____null_761615.jpg'
img=cv2.imread(f)

show(img)
img=gamma_trans(img,1)

show(img)

