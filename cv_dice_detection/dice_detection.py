"""
dice_detection.py

DiceDetection is a Python package for detecting and analyzing dice in images or video streams.

This module provides a DiceDetection class that encapsulates functionalities for dice detection,
including blob detection, clustering, and result announcement using text-to-speech.

Dependencies:
    - OpenCV (cv2)
    - NumPy (numpy)
    - scikit-learn (sklearn)
    - Calibration (calibration)
    - Configuration Settings (configs)
    - Google Text-to-Speech (gtts)
    - Pygame (pygame)

Usage:
    To use this package, create an instance of the DiceDetection class, calibrate the distance
    parameter using `calibrate_distance`, and then use the various methods provided for blob
    detection, result extraction, and display.

Example:
    * Create an instance of DiceDetection
    
    dice_detector = DiceDetection()

    * Calibrate the distance parameter
    
    dice_detector.calibrate_distance(35)

    * Get blobs from a frame
    
    frame = cv2.imread("dice_image.jpg")
    blobs = dice_detector.get_blobs(frame)

    * Get dice information from blobs
    
    dice_info, num_dice = dice_detector.get_dice_from_blobs(blobs)

    * Overlay information on the frame
    
    dice_detector.overlay_info(frame, dice_info, blobs)

    * Stop detection when stable state is reached
    
    self.sum_list, already_printed = dice_detector.stop_detection(num_dice, self.sum_list, already_printed, frame)

    * Announce the result using text-to-speech
    
    dice_detector.announce_result(num_dice)

    * Display text on the frame
    
    dice_detector.show_on_image(frame, "Dice detection in progress...")
"""

from io import BytesIO

import cv2
import numpy as np
import pygame
from gtts import gTTS
from sklearn import cluster
import asyncio

from calibration import MEDIANBLUR, MININERTIARATIO, SUM_THRESHOLD, CAMERA_DISTANCE


class DiceDetection:
    """DiceDetection is a Python package for detecting and
        analyzing dice in images or video streams.

    Attributes:
        detector: Instance of cv2.SimpleBlobDetector for blob detection.
        distance_parameter (float): Parameter used for DBSCAN clustering, calibrated based on camera distance.
    """

    def __init__(self):
        """Initialize the DiceDetection object.

        The constructor sets up parameters for blob detection and
            initializes the distance_parameter.
        """
        self.sum_list = []
        self.params = cv2.SimpleBlobDetector_Params()
        self.params.filterByInertia
        self.params.minInertiaRatio = MININERTIARATIO
        self.detector = cv2.SimpleBlobDetector_create(self.params)
        # Extract appropriate EPS value for DBSCAN clustering. 70 for 30 cm and 50 for 40 cm
        self.distance_parameter: float = 70 - (CAMERA_DISTANCE - 30) * 2

    def calibrate_distance(self, distance: float):
        """Calibrate the distance parameter after instantiation.

        Args:
            distance (float): Distance between the camera and the white table. Range: 30-40 cm.
        """
        self.distance_parameter = 70 - (distance - 30) * 2

    def get_blobs(self, frame: np.ndarray) -> list:
        """Detect blobs in the input frame.

        Args:
            frame (numpy.ndarray): Input image frame.

        Returns:
            list: List of detected blobs.
        """
        frame_blurred = cv2.medianBlur(frame, MEDIANBLUR)
        frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
        blobs = self.detector.detect(frame_gray)

        return blobs

    def get_dice_from_blobs(self, blobs: list) -> (list, int):
        """Extract dice information from detected blobs.

        Args:
            blobs (list): List of detected blobs.

        Returns:
            tuple: A tuple containing a list of dice information and the number of dice.
        """
        pos_list = []
        for b in blobs:
            pos = b.pt

            if pos is not None:
                pos_list.append(pos)

        pos_list = np.asarray(pos_list)

        if len(pos_list) > 0:
            clustering = cluster.DBSCAN(eps=self.distance_parameter, min_samples=1).fit(
                pos_list
            )
            num_dice = max(clustering.labels_) + 1
            dice = []
            sum = 0
            for i in range(num_dice):
                x_dice = pos_list[clustering.labels_ == i]
                sum += len(x_dice)
                centroid_dice = np.mean(x_dice, axis=0)
                dice.append([len(x_dice), *centroid_dice])

            return dice, num_dice, sum
        return [], 0, 0

    def stop_detection(
        self,
        num_dice: int,
        already_printed: bool,
        frame: np.ndarray,
        sum: int,
    ) -> (list, bool):
        """Stop dice detection when a stable state is reached.

        Args:
            num_dice (int): Number of dice detected.
            self.sum_list (list): List to track the sum of dice over time.
            already_printed (bool): Flag to avoid redundant printing.
            frame (numpy.ndarray): Input image frame.

        Returns:
            tuple: A tuple containing the updated self.sum_list and already_printed flags.
        """
        self.sum_list.append(num_dice)

        are_all_same = False

        if len(self.sum_list) > SUM_THRESHOLD:
            self.sum_list.pop(0)
            are_all_same = all(s == self.sum_list[0] for s in self.sum_list)

        if are_all_same:
            if not already_printed:
                print(self.sum_list)
                print("The dice has stopped. Its final value is: " + str(sum))
                self.announce_result(sum)
                print("Finished accounce result")
                already_printed = True
            text = "Dice sum: " + str(sum)
            self.show_on_image(frame, text)
            return self.sum_list, already_printed
        already_printed = False
        text = "Loading..."
        self.show_on_image(frame, text)
        return self.sum_list, already_printed

    def overlay_info(self, frame: np.ndarray, dice: list, blobs: list):
        """Overlay information on the input frame.

        Args:
            frame (numpy.ndarray): Input image frame.
            dice (list): List of dice information.
            blobs (list): List of detected blobs.
        """
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

    def announce_result(self, number: int) -> None:
        """Announce the result using text-to-speech.

        Args:
            number (int): Result to be announced.
        """
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
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)
        return

    def show_on_image(self, frame: np.ndarray, text: str):
        """Display text on the input frame.

        Args:
            frame (numpy.ndarray): Input image frame.
            text (str): Text to be displayed.
        """
        cv2.putText(
            frame,
            text,
            (40, 50),
            cv2.FONT_HERSHEY_PLAIN,
            4,
            (0, 255, 0),
            4,
        )
