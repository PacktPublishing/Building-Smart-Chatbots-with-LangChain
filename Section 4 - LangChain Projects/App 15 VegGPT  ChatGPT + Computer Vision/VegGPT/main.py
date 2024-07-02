import argparse
import tkinter as tk
from tkinter import filedialog
import asone 
from functionfiles import * 
import cv2
from numpy import random
import numpy as np
from asone.utils import *
import openai

openai.api_key = "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"

def generate_recipe(ingredients):
    ingredients_str = ', '.join(ingredients)
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role":"system", "content": "Take these ingredients" + ingredients_str},
            {"role": "user", "content": "Generate me a recipe based on these ingredients."},
        ]
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content

    print(result)
    return result


def detect_ingredients(args):
    filter_classes = None
    detection = asone.ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8L_PYTORCH,weights='best.pt',use_cuda=True)
    # Get tracking function
    tracking = detection.track_video(args.video_path,output_dir='data/results',conf_thres=0.25,iou_thres=0.45,display=True,draw_trails=True,filter_classes=filter_classes,class_names=[]) 
    # Loop over track_fn to retrieve outputs of each frame 
    for bbox_details, frame_details, vegetables in tracking:
        bbox_xyxy, ids, scores, class_ids = bbox_details
        frame, frame_num, fps = frame_details

    vegetable_names = list(map(str, vegetables.keys()))
    ingredients = vegetable_names
    print("Ingredients")
    print(ingredients)
    recipe = generate_recipe(ingredients)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('video_path', help='Path to input video')
    args = parser.parse_args()

    detect_ingredients(args)
