import cv2
import numpy
import bm3d
from matplotlib import pyplot as plt
import pprint
import os
import rmidi
from rmidi.muse import Muse


def get_image_edges(filepath, inverse = False, plot = True, filename = "default.png"):
    img = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, int(128 * img.shape[0] / img.shape[1])), interpolation = cv2.INTER_NEAREST)
    
    # img = bm3d.bm3d(img, sigma_psd=30/255, stage_arg=bm3d.BM3DStages.HARD_THRESHOLDING)
    edges = cv2.Canny(img,200,200)
    
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()
    return edges


def read_img_to_matrix(filepath):
    print("reading image to matix")
    img = cv2.imread(filepath, 0)
    # pprint.pprint(list(img))
    return img

def write_matrix_to_img(img, filename, dir = "."):
    print(os.path.join(dir, filename))
    cv2.imwrite(os.path.join(dir, filename), img)
    return True

def img_to_midi2(filepath, name = "default2") :
    if isinstance(filepath, str): img = get_image_edges(filepath)
    else : 
        img = filepath
        filepath = name
    notes_on = set()
    midi_notes_sequence = []
    notes_time = numpy.zeros(128, dtype = "int32")
    for i in range(img.shape[0] - 1, -1, -1):
        high_indexes = set(numpy.where(img[i] > 0)[0])
        print(f"high indexs  : ", high_indexes)
        notes_off = notes_on - high_indexes
        for note in notes_off:
            midi_notes_sequence.append([note, notes_time[note]])
        notes_on = high_indexes
        notes_time[list(notes_on)] += 1
    midi_notes_sequence = numpy.array(midi_notes_sequence)
    midiobj = Muse.muse(midi_notes_sequence[:, 1] * 2, midi_notes_sequence[:, 0], kind="tick", oftype= "melody")
    midiobj.create_file(filepath + ".mid")

def img_to_midi(filepath, name = "default", edge = True, offset = 0, threshold = 100):
    if isinstance(filepath, str) and not edge: img = get_image_edges(filepath, filename=name)
    elif edge and isinstance(filepath, str) : img = read_img_to_matrix(filepath)
    else : 
        img = filepath
        filepath = name
    img_cp = img.copy()
    img_cp[img > threshold] = 255
    img_cp[img <= threshold] = 0
    img = img_cp
    plt.imshow(img, cmap='gray')
    prev_high_indexes = set() # set of notes that are pressed
    midi_notes_sequence = []
    mid = rmidi.MIDI()
    notes_time = numpy.zeros(128, dtype = "int32")
    delta = 0
    plt.imshow(img, cmap='gray')
    plt.show()
    for i in range(img.shape[0] - 1, -1, -1):
        # print("--" * 50)
        # print("delta : ", delta)
        curr_high_indexes = set(numpy.where(img[i] > threshold)[0]) # number of high notes at moments
        
        notes_off = prev_high_indexes - curr_high_indexes # number of notes off at moment, diff between prev & curr high
        for note in notes_off:
            midi_notes_sequence.append([note, notes_time[note]])
            # try : 
            # print(f"Note Off [{note + offset}] : delta => [{delta}]")
            mid.track(0).add_event(delta, 'note_on', note_number = note + offset, velocity = 0, channel_no = 0, kind = 'tick')
            delta = 0
            # except ZeroDivisionError:
            #     mid.track(0).add_event(0, 'note_on', note_number = note, velocity = 90, channel_no = 0, kind = 'note')
            

        notes_on  = curr_high_indexes - prev_high_indexes # number of new high notes / just presssed this moment, rever
        for note in notes_on:
            # try :
            # print(f"Note On [{note + offset}] : delta => [{delta}]")
            mid.track(0).add_event(delta, 'note_on', note_number = note + offset, velocity = 90, channel_no = 0, kind = 'tick')
            # except ZeroDivisionError: 
            #     mid.track(0).add_event(0, 'note_on', note_number = note, velocity = 90, channel_no = 0, kind = 'note')
            delta = 0
        
        # print(f"note on : {numpy.array(list(notes_on)) + offset}")
        # print(f"note off : {numpy.array(list(notes_off)) + offset}")
        # print(f"prev high : {numpy.array(list(prev_high_indexes)) + offset}")
        # print(f"curr_high : {numpy.array(list(curr_high_indexes)) + offset}")
        # print("--" * 50)
        prev_high_indexes = curr_high_indexes # number of high index at current movement

        notes_time[list(notes_on)] += 1
        delta += 32
    midi_notes_sequence = numpy.array(midi_notes_sequence)
    # midiobj = Muse.muse(midi_notes_sequence[:, 1] * 2, midi_notes_sequence[:, 0], kind="tick", oftype= "melody")
    # midiobj.create_file(filepath + ".mid")
    print(mid)
    mid.compress(filepath + ".mid")
