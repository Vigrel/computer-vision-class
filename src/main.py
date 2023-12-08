from DiceDetection import DiceDetecion
import cv2
import numpy as np
from fastapi import FastAPI
import uvicorn
from sklearn.cluster import DBSCAN
import asyncio

app = FastAPI()

@app.get("/dice-detection")
@app.route('/')

async def main():
    captured = cv2.VideoCapture(0)
    dice_detector = DiceDetecion()

    while True:
        ret, frame = captured.read()

        if not ret:
            print("Error reading frame from the camera")
            break

        blobs = await dice_detector.get_blobs(frame)
        dice = await dice_detector.get_dice_from_blobs(blobs)
        await dice_detector.overlay_info(frame, dice, blobs)

        print(dice)

        cv2.imshow("frame", frame)

        res = cv2.waitKey(1)

        if res & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    uvicorn.run(app, host="127.0.0.1", port=8000)