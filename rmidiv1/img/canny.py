import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_image_edges(filepath, inverse = False, plot = True):

    img = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
    print("img : ", img.shape)
    print("res shape : ", (128, int(128 * img.shape[0] / img.shape[1])))
    img_res = cv2.resize(img, (128, int(128 * img.shape[0] / img.shape[1])), interpolation = cv2.INTER_NEAREST)
    edges = cv2.Canny(img_res,200,200)
    print (edges.shape)
    # kernel = np.ones((3,3),np.float32)/9
    # dst = cv2.filter2D(edges,-1,kernel)
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

def read_img_to_matrix(filepath):
    img = cv2.imread(filepath, 0)
    print(img)