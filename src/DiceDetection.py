import cv2
import numpy as np
from sklearn import cluster
from calibration import *
from configs import CAMERA_DISTANCE
from gtts import gTTS
import pygame
from io import BytesIO

global sum_list

class DiceDetecion:

    def __init__(self):
        self.params = cv2.SimpleBlobDetector_Params()
        self.params.filterByInertia
        self.params.minInertiaRatio = MININERTIARATIO
        self.detector = cv2.SimpleBlobDetector_create(self.params)
        # Formula to extract the appropriate EPS value for DBSCAN clustering, which is 70 for 30 cm and 50 for 40 cm
        self.distance_parameter = 70 - (CAMERA_DISTANCE - 30) * 2

    def calibrate_distance(self, distance):
        """Function used to calibrate the distance parameter after instantiation

        Args:
            distance (int): distance between the camera and the white table. Range: 30-40 cm
        """
        self.distance_parameter = 70 - (distance - 30) * 2

    async def get_blobs(self, frame):
        """this function glaubers"""
        frame_blurred = cv2.medianBlur(frame, MEDIANBLUR)
        frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
        blobs = self.detector.detect(frame_gray)

        return blobs

    async def get_dice_from_blobs(self, blobs):
        X = []
        for b in blobs:
            pos = b.pt

            if pos != None:
                X.append(pos)

        X = np.asarray(X)

        if len(X) > 0:
            clustering = cluster.DBSCAN(eps=self.distance_parameter, min_samples=1).fit(
                X
            )
            num_dice = max(clustering.labels_) + 1
            dice = []

            for i in range(num_dice):
                X_dice = X[clustering.labels_ == i]
                centroid_dice = np.mean(X_dice, axis=0)
                dice.append([len(X_dice), *centroid_dice])

            return dice, num_dice
        else:
            return [], 0

    async def stop_detection(self, num_dice, sum_list, already_printed, frame):
        sum_list.append(num_dice)

        are_all_same = False
        
        print(num_dice)

        if len(sum_list) > SUM_TRESHOLD:
            sum_list.pop(0)
            are_all_same = all(s == sum_list[0] for s in sum_list)

        if are_all_same:
            if not already_printed:
                print(sum_list)
                print("The dice has stopped. Its final value is: " + str(num_dice))
                await self.announce_result(num_dice)
                already_printed = True
            text = "Dice sum: " + str(num_dice)
            self.show_on_image(frame, text)
            return sum_list, already_printed
        else:
            already_printed = False
            text = "Loading..."
            self.show_on_image(frame, text)
            return sum_list, already_printed

    async def overlay_info(self, frame, dice, blobs):
        for b in blobs:
            pos = b.pt
            r = b.size / 2
            cv2.circle(frame, (int(pos[0]), int(pos[1])), int(r), (255, 0, 0), 2)

        for d in dice:
            textsize = cv2.getTextSize(str(d[0]), cv2.FONT_HERSHEY_PLAIN, 3, 2)[0]
            cv2.putText(
                frame,
                str(d[0]),
                (int(d[1] - textsize[0] / 2), int(d[2] + textsize[1] / 2)),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 255, 0),
                2,
            )

    async def announce_result(self, number):
        tts = gTTS(text=f"{number} rolled", lang="en", slow=False)
        # Save the audio to a BytesIO object
        audio_stream = BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Load the audio stream
        pygame.mixer.music.load(audio_stream)

        # Play the audio
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return

    def show_on_image(self, frame, text):
        cv2.putText(
            frame,
            text,
            (40, 50),
            cv2.FONT_HERSHEY_PLAIN,
            4,
            (0, 255, 0),
            4,
        )
