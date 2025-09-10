import math
import json
import srt
import pickle
from backend.speech_bubble.lip_detection import get_lips
from backend.speech_bubble.bubble_placement import get_bubble_position
from backend.speech_bubble.bubble_shape import get_bubble_type
from backend.class_def import bubble
import threading


def bubble_create(video, crop_coords, black_x, black_y):

    bubbles = []


    # def bubble_create(bubble_cord,lip_cord,page_template):
    data=""
    with open("test1.srt") as f:
        data=f.read()
    subs=srt.parse(data)


    # Reading CAM data from dump
    CAM_data = None
    with open('CAM_data.pkl', 'rb') as f:
        CAM_data = pickle.load(f)

    lips = get_lips(video, crop_coords,black_x,black_y)
    # Dumping lips
    with open('lips.pkl', 'wb') as f:
        pickle.dump(lips, f)

    # # Reading lips
    # lips=None
    # with open('lips.pkl', 'rb') as f:
    #     lips = pickle.load(f)
    
    # emotion_thread.join()
    # print("Detected emotions:", emotions)


    for sub in subs:
        try:
            # Check if we have lip data for this subtitle
            if sub.index < len(lips) and lips[sub.index] is not None and len(lips[sub.index]) >= 2:
                lip_x = lips[sub.index][0]
                lip_y = lips[sub.index][1]
            else:
                lip_x = -1
                lip_y = -1

            # Check if we have crop coordinates and CAM data for this subtitle
            if sub.index-1 < len(crop_coords) and sub.index-1 < len(CAM_data):
                bubble_x, bubble_y = get_bubble_position(crop_coords[sub.index-1], CAM_data[sub.index-1])
            else:
                bubble_x = 0
                bubble_y = 0

            dialogue = sub.content
            emotion = get_bubble_type(dialogue)
            print(f'||emotion:{emotion}||')

            temp = bubble(bubble_x, bubble_y,lip_x,lip_y,sub.content,emotion)
            bubbles.append(temp)
            
        except Exception as e:
            print(f"Error processing subtitle {sub.index}: {e}")
            # Create a default bubble
            temp = bubble(0, 0, -1, -1, sub.content, "normal")
            bubbles.append(temp)

    return bubbles









