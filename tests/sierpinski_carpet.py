from fractal.generation import SierpinskiCarpet
from fractal.generation import Plot
import logging
import os
import cv2
import imagezmq

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s [%(levelname)s] %(message)s')

def main():
    logging.info("sierpinski_carpet.py main()")
    output_directory = './outputs'
    number_of_points = 100000
    image_sizeHW= (1024, 1024)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    sender = imagezmq.ImageSender(connect_to="tcp://127.0.0.1:5555", REQ_REP=True)

    sierpiski_generator = SierpinskiCarpet()
    logging.info("Generating points...")
    points = sierpiski_generator.GeneratePoints(number_of_points=number_of_points, number_of_points_to_ignore=10)
    image = Plot(points, image_sizeHW)
    sender.send_image("sierpinski", image)

    for step in range(10):
        logging.info("Generating points...")
        new_points = sierpiski_generator.GeneratePoints(number_of_points=number_of_points,
                                                        number_of_points_to_ignore=0, first_point=points[-1])
        logging.info("Done!")
        #points = points + new_points
        logging.info("Plotting in an image...")
        image = Plot(new_points, image=image)
        logging.info("Done!")

        sender.send_image("sierpinski", image)
    image_filepath = os.path.join(output_directory, "sierpinski_{}.png".format(number_of_points))
    cv2.imwrite(image_filepath, image)

if __name__ == '__main__':
    main()