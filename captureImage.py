import cv2
import time

def captureImage():
    cam = cv2.VideoCapture(0)
    # if not cam.isOpened():
    #     cam = cv2.VideoCapture(0)

    time.sleep(3) #time.sleep is added to take a bright image
    if not cam.isOpened():
        raise IOError("Cannot open the webcam")

    result,image = cam.read()

    if result:
        # return the image in jpg format
        cv2.imwrite('static/images/captured_image.jpg', image)

    else:
        print("Camera not working")

    return 'static/images/captured_image.jpg'