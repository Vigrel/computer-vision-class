from DiceDetection import DiceDetecion
import cv2


def main():
    captured = cv2.VideoCapture(0)
    dice_detector = DiceDetecion()

    while True:
        ret, frame = captured.read()

        blobs = dice_detector.get_blobs(frame)
        dice = dice_detector.get_dice_from_blobs(blobs)
        dice_detector.overlay_info(frame, dice, blobs)
        print(dice)
        cv2.imshow("frame", frame)

        res = cv2.waitKey(1)

        if res & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()
