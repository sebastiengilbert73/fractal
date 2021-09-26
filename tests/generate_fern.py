import logging
import fractal.models.fern as fern
from fractal.generation import Plot
import os
import cv2

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s [%(levelname)s] %(message)s')

def main():
    logging.info("generate_fern.py main()")

    output_directory = './outputs'

    simple_fern = fern.SimpleFern()
    points = simple_fern.GeneratePoints(
        number_of_points=100000,
        number_of_points_to_ignore=10,
        first_point=None)
    fern_img = Plot(points, image_sizeHW=(512, 512), range_x=(-5, 2), range_y=(-1, 6))
    fern_img_filepath = os.path.join(output_directory, "fern.png")
    cv2.imwrite(fern_img_filepath, fern_img)

if __name__ == '__main__':
    main()