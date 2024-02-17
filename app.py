# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m5KFDcKlTwXAj0Hmr8kWBWYXWOycolsE
"""

!pip install moviepy
!pip install opencv-python
!pip install tensorflow

import numpy as np
import cv2
from moviepy.editor import VideoFileClip
from IPython.display import HTML
from keras.models import load_model

# Class to average lanes with
class Lanes():
    def __init__(self):
        self.recent_fit = []
        self.avg_fit = []


def road_lines(image):

    # Get image ready for feeding into model
    small_img = cv2.resize(image, (160, 80))
    small_img = np.array(small_img)
    small_img = small_img[None,:,:,:]

    # Make prediction with neural network (un-normalize value by multiplying by 255)
    prediction = model.predict(small_img)[0] * 255

    # Add lane prediction to list for averaging
    lanes.recent_fit.append(prediction)
    # Only using last five for average
    if len(lanes.recent_fit) > 5:
        lanes.recent_fit = lanes.recent_fit[1:]

    # Calculate average detection
    lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis = 0)

    # Generate fake R & B color dimensions, stack with G
    blanks = np.zeros_like(lanes.avg_fit).astype(np.uint8)
    lane_drawn = np.dstack((blanks, lanes.avg_fit, blanks))

    # Re-size to match the original image
    lane_image = cv2.resize(lane_drawn, (1280, 720))

    # Merge the lane drawing onto the original image
    result = cv2.addWeighted(image, 1, lane_image, 1, 0, dtype=cv2.CV_8UC3)

    return result


if __name__ == '__main__':
    # Load Keras model
    model = load_model('/content/full_CNN_model.h5')
    # Create lanes object
    lanes = Lanes()

    # Where to save the output video
    vid_output = 'proj_reg_vid.mp4'
    # Location of the input video
    clip1 = VideoFileClip("/content/challenge_video.mp4")
    # Create the clip
    vid_clip = clip1.fl_image(road_lines)
    vid_clip.write_videofile(vid_output, audio=False)

!pip install streamlit
