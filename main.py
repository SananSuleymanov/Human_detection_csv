#!/usr/bin/env python3

import cv2

import torch
from datetime import datetime
import csv

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
cap = cv2.VideoCapture(0)


class occupancy:
    def __init__(self):
        self.num =0
        self.difference =0
        self.old_time =0
        self.current_time =0
        self.time2 =0


    def boxes(self, interval):
        time1 = datetime.now()
        while True:
            self.num = 0
            ret, image = cap.read()
            if ret:
                try:
                    result = model(image)
                    for i in range(result.xyxy[0].numpy().shape[0]):

                        if result.xyxy[0].numpy()[i][5] == 0:
                            xmin = int(result.xyxy[0].numpy()[i][0])
                            ymin = int(result.xyxy[0].numpy()[i][1])
                            xmax = int(result.xyxy[0].numpy()[i][2])
                            ymax = int(result.xyxy[0].numpy()[i][3])
                            start_point = (xmin, ymin)
                            end_point = (xmax, ymax)
                            cv2.rectangle(image, start_point, end_point, (255, 0, 0), 2)
                            cv2.imshow('Image', image)
                            self.num += 1
                            self.time2 = datetime.now()
                            self.old_time = time1.strftime("%M")
                            self.current_time = self.time2.strftime("%M")

                            print("Old time: ", self.old_time)
                            print("Current time: ", self.current_time)
                            self.difference = int(self.current_time) - int(self.old_time)
                            print("Difference: ", self.difference)

                    if self.difference == interval:
                        self.counter()
                        print("The number of people is determined")
                        time1 = self.time2
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except:
                    print("Not possible to run model")
    def counter(self):
        time_raw = datetime.now()
        times = time_raw.strftime("%d-%m-%Y %H:%M:%S")

        i = 1
        print(self.num, times)
        data = [times, self.num]
        with open("data.csv", "a", encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)



while True:
    occupant = occupancy()
    occupant.boxes(5)


