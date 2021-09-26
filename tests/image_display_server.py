import cv2
import imagezmq

image_hub = imagezmq.ImageHub()
while True:
    msg, image = image_hub.recv_image()
    cv2.imshow(msg, image)
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')