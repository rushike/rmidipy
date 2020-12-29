from . import functions, canny, shapes
import matplotlib.pyplot as plt
import cv2

def test_canny_get_image_edges(filepath = "face_img.png"):
    edges = functions.get_image_edges(filepath)
    functions.write_matrix_to_img(edges, filepath.split(".")[0] + "1.png") # write the image
# test_canny_get_image_edges("modi-cartoon.webp") 
# test_canny_get_image_edges("trump.jpg")   

def test_read_img_to_matrix(filepath = "face_img.png"):
    functions.read_img_to_matrix(filepath)
# test_read_img_to_matrix()

def test_img_to_midi(filepath = "face_img.png", edge = True, offset = 24, threshold = 100):
    functions.img_to_midi(filepath, ".".join([filepath.split(".")[0], "png"]), edge= edge, offset=offset, threshold=threshold)
# test_img_to_midi()
# test_img_to_midi("modi-cartoon1.png", edge = True)
# test_img_to_midi("trump1.png", edge = True)
# test_img_to_midi("Alphabet Fall On.png", edge = True, offset = 24)
test_img_to_midi("Image-Note.png", edge = True, offset = 48, threshold=230)

def test_circle_to_midi():
    img = shapes.get_circle((48, 48), 15, 128, 128)
    functions.img_to_midi(img, name = "circle.png")
    plt.imshow(img, cmap = 'gray')
    plt.show()
# test_circle_to_midi()

def test_draw_unicode():
    shapes.draw_unicode()
# test_draw_unicode()

def test_draw_alphabet():
    img = shapes.draw_aplhabets()
    cv2.imwrite("alphabet.png", img)
# test_draw_alphabet()