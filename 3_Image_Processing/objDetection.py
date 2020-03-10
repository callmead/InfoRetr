#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 20:27:58 2018

@author: afarhan
"""

from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()


detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
detector.loadModel()
for filename in os.listdir(execution_path):
    if filename.endswith(".jpg"): 
        inputPath = os.path.join(execution_path, filename)
        outputPath = os.path.join(execution_path,'out'+ filename)
        detections = detector.detectObjectsFromImage(input_image=inputPath, output_image_path=outputPath, minimum_percentage_probability=30)
    else:
        continue



for eachObject in detections:
    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    print("--------------------------------")