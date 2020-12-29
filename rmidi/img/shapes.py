import cv2
import numpy
import string
import matplotlib.pyplot as plt

def get_black_image(w, h):
    return numpy.zeros((w, h))

def get_shape(name):
    pass

def get_circle(center, radius, w, h, **kwargs):
    """Draw the circle

    Args:
        center ([tuple of int]): center of the circle
        radius ([int]): radius of the circle
        w ([int]): width of image (in X - direction)
        h ([int]): height of image (in Y - direction)
    Keyword Argument : 
        color ([tuple of int]) : RGB color value in tuple() [default : (255, 255, 255)]
        thickness ([int]) : integer specifies the thickness of line (in pixels) [default : 1]
    """
    img = get_black_image(w, h)
    color = kwargs.get('color', (255, 255, 255))
    thickness = kwargs.get('thickness', 1)
    return cv2.circle(img, center, radius, color, thickness)

def draw_unicode(text = "G", **kwargs):
    thickness = kwargs.get("thickness", 20)
    img = numpy.zeros((480, 480))
    print("unicode drwaing ...")

    cv2.putText(img, text, (20,450), cv2.FONT_HERSHEY_SIMPLEX,20,(255,255,255),thickness)
    img = cv2.resize(img, (13, 13), interpolation = cv2.INTER_NEAREST)
    # img = cv2.resize(img, (13, 21), interpolation = cv2.INTER_NEAREST)
    # plt.imshow(img, cmap = 'gray')
    # plt.show()
    return img

def draw_aplhabets():
    """
     ---------------------→ Y
    |
    |
    |
    |
    |
    |
    🠗
    X
    """
    img = numpy.zeros((450, 88))
    x_iter = 5
    y_iter = 0
    incr = 13
    alpha_list = list(string.ascii_uppercase)
    alpha_list.reverse()
    for char in alpha_list:
        char_img = draw_unicode(char)
        print(f"PREV : x_iter : {x_iter}, y_iter : {y_iter}, incr : {incr}")
        if y_iter + 13 > 85:
            incr = -13
        if y_iter - 13 < 5:
            incr = 13
        y_iter += incr
        x_iter += 13
        print(f"x_iter : {x_iter}, y_iter : {y_iter}, incr : {incr}")
        img[x_iter : x_iter + 13, y_iter - 13 :y_iter] = char_img

    plt.imshow(img, cmap= 'gray')
    plt.show()
    return img
        


