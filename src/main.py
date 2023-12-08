from DiceDetection import DiceDetecion
import cv2
import numpy as np
import uvicorn
import asyncio
import time


async def main(*args):
    captured = cv2.VideoCapture(0)
    dice_detector = DiceDetecion()

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
