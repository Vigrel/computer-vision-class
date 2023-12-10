"""
dice_detection_demo.py

This script provides a simple demonstration of using the DiceDetection package for real-time
dice detection using a webcam.

Usage: Run this script to start the real-time dice detection. Press 'q' to exit the application.

Example:
    $ python dice_detection_demo.py
"""

from dice_detection import DiceDetection
import cv2
import asyncio

async def main(*args):
    """Main function for real-time dice detection using a webcam.

    This function initializes the camera, creates an instance of DiceDetection,
    and continuously processes frames for dice detection.

    Args:
        *args: Additional command-line arguments.
    """
    captured = cv2.VideoCapture(0)
    dice_detector = DiceDetection()

    sum_list = []

    already_printed = False

    while True:
        ret, frame = captured.read()

        if not ret:
            print("Error reading frame from the camera")
            break

        blobs = await dice_detector.get_blobs(frame)
        dice, sum = await dice_detector.get_dice_from_blobs(blobs)
        sum_list, already_printed = await dice_detector.stop_detection(
            sum, sum_list, already_printed, frame
        )
        await dice_detector.overlay_info(frame, dice, blobs)

        cv2.imshow("frame", frame)

        res = cv2.waitKey(1)

        if res & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()