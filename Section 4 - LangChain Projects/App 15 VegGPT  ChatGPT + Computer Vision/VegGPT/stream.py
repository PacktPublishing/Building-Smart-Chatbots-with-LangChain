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
import os
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

openai.api_key = "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"


class RecipeMainWindow(customtkinter.CTk):
    def detect_ingredients(self,video_path):
        filter_classes = None
        detection = asone.ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8L_PYTORCH,weights='best.pt',use_cuda=True)
        # Get tracking function
        tracking = detection.track_video(video_path,output_dir='data/results',conf_thres=0.85,iou_thres=0.85,display=True,draw_trails=True,filter_classes=filter_classes,class_names=[]) 
        # Loop over track_fn to retrieve outputs of each frame 
        for bbox_details, frame_details, vegetables in tracking:
            bbox_xyxy, ids, scores, class_ids = bbox_details
            frame, frame_num, fps = frame_details

        vegetable_names = list(map(str, vegetables.keys()))
        ingredients = vegetable_names
        print("Ingredients")
        print(ingredients)
        recipe = self.generate_recipe(ingredients)
        
        # Create a label with the recipe
        self.recipe_label.configure(text=recipe)

    def generate_recipe(self,ingredients):
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

    def select_video(self):
        # Show a file dialog to choose a video file
        file_path = filedialog.askopenfilename(title="Select Video", filetypes=(("Video files", "*.mp4;*.m4v;*.mov"), ("All files", "*.*")))
        self.detect_ingredients(file_path)
        
    def __init__(self):
        super().__init__()

        self.title("Vision AI Recipe Generator")
        self.geometry("700x500")
        self.configure(bg="#EFEFEF")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create button and label
        self.select_button = customtkinter.CTkButton(self, text="Select video", command=self.select_video)
        self.recipe_label = customtkinter.CTkLabel(self, text="Your Recipe will be generated here.")
       

        self.frame = customtkinter.CTkFrame(self, corner_radius=20, fg_color="transparent")

    
        self.frame.grid()
        self.select_button.grid(row=2, column=0, padx=10, pady=(0,30))
        self.recipe_label.grid(row=1, column=0, padx=10, pady=(0,30))


if __name__ == '__main__':
    # Create a new window
    app = RecipeMainWindow()

    app.mainloop()

    # Run the window
    window.mainloop()
