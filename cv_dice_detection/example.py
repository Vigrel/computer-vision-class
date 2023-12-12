import cv2 as cv
import numpy as np

# from mtcnn.mtcnn import MTCNN
from flask import Flask, render_template
from flask_sock import Sock
import asyncio

# detector = MTCNN()
app = Flask(__name__)
sock = Sock(app)
from dice_detection import DiceDetection

dice_detector = DiceDetection()
already_printed = False
@app.route("/")
def index():
    return render_template("example.html")


@sock.route("/socket")
def echo(socket):
    while True:
        input_data = socket.receive()
        input_array = np.frombuffer(input_data, np.uint8)
        input_image = cv.imdecode(input_array, cv.IMREAD_COLOR)
        output_image = process(input_image)
        _, output_array = cv.imencode(".png", output_image)
        output_data = output_array.tobytes()
        socket.send(output_data)


def process(input_image):
    blobs = dice_detector.get_blobs(input_image)
    dice, num_dice, sum = dice_detector.get_dice_from_blobs(blobs)
    dice_detector.stop_detection(
        num_dice, already_printed, input_image, sum
    )
    dice_detector.overlay_info(input_image, dice, blobs)

    return input_image
