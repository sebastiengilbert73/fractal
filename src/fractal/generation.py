import numpy as np
import cv2
import string
import random


def Transform(transformation_mtx, translation_vct, xy):
    if transformation_mtx.shape != (2, 2):
        raise ValueError("Transform(): transformation_mtx.shape ({}) != (2, 2)".format(transformation_mtx.shape))
    if translation_vct.shape != (2, 1):
        raise ValueError("Transform(): translation_vct.shape ({}) != (2, 1)".format(translation_vct.shape))
    if xy.shape != (2, 1):
        raise ValueError("Transform(): xy.shape ({}) != (2, 1)".format(xy.shape))
    return transformation_mtx @ xy + translation_vct

def Plot(points, image_sizeHW=None, image=None, range_x=None, range_y=None):

    if range_x is None:
        xs = [p[0] for p in points]
        range_x = (min(xs), max(xs))
    if range_y is None:
        ys = [p[1] for p in points]
        range_y = (min(ys), max(ys))
    if image is None:
        image = np.zeros((image_sizeHW[0], image_sizeHW[1], 3))
    else:
        image_sizeHW = (image.shape[0], image.shape[1])
    for p in points:
        x_pixel = round( (image_sizeHW[1] - 1) * (p[0] - range_x[0])/(range_x[1] - range_x[0]))
        y_pixel = round( (image_sizeHW[0] - 1) * (p[1] - range_y[0]) / (range_y[1] - range_y[0]))
        if x_pixel >= 0 and x_pixel < image_sizeHW[1] and y_pixel >= 0 and y_pixel < image_sizeHW[0]:
            image[y_pixel, x_pixel] = (0, 255, 0)
    return image

class IterativeTransformer():
    """
    A fractal generator that iteratively apply a randomly chosen affine transformation
    """

    def __init__(self, transformation_tuples_list=None, corresponding_probabilities=None):
        self.characters = string.ascii_letters + string.digits
        self.name_to_transformations = {}
        self.name_to_probability = {}
        if transformation_tuples_list is not None:
            if corresponding_probabilities is not None:
                if len(corresponding_probabilities) != len(transformation_tuples_list):
                    raise ValueError("IterativeTransformer.__init__(): len(corresponding_probabilities) ({}) != len(transformation_tuples_list) ({})".format(len(corresponding_probabilities), len(transformation_tuples_list)))
            for transformationNdx in range(len(transformation_tuples_list)):
                name = ''.join(random.choice(self.characters) for i in range(10))  # Cf. https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
                self.name_to_transformations[name] = transformation_tuples_list[transformationNdx]
                if corresponding_probabilities is None:
                    self.name_to_probability[name] = 1.0/len(transformation_tuples_list)
                else:
                    self.name_to_probability[name] = corresponding_probabilities[transformationNdx]
        else:
            self.__init__( [ (np.array([[1, 0], [0, 1]]), np.array([0, 0])) ] )
        self.NormalizeProbabilities()

    def NormalizeProbabilities(self):
        sum = 0
        for name, prob in self.name_to_probability.items():
            sum += prob
        for name, prob in self.name_to_probability.items():
            normalized_prob = prob/sum
            self.name_to_probability[name] = normalized_prob

    def RandomlyChooseTransformation(self):
        random_nbr = random.random()
        sum = 0
        chosen_transformation_name = None
        for name, prob in self.name_to_probability.items():
            sum += prob
            if sum >= random_nbr:
                chosen_transformation_name = name
                break
        return self.name_to_transformations[chosen_transformation_name]

    def GeneratePoints(self, number_of_points, number_of_points_to_ignore,
                 first_point=None):
        generated_points = []
        if first_point is None:
            current_point = np.random.random((2, 1))
        else:
            current_point = np.array([[first_point[0]], [first_point[1]]])
        for ptNdx in range(number_of_points + number_of_points_to_ignore):
            transformation_mtx, translation_vct = self.RandomlyChooseTransformation()
            next_point = Transform(transformation_mtx, translation_vct, current_point)
            if ptNdx >= number_of_points_to_ignore:
                generated_points.append((next_point[0][0], next_point[1][0]))
            current_point = next_point
        return generated_points

class SierpinskiCarpet(IterativeTransformer):
    def __init__(self):
        transformation_tuples_list = [
            (np.array([[1/3, 0], [0, 1/3]]), np.array([[0], [0]])),
            (np.array([[1 / 3, 0], [0, 1 / 3]]), np.array([[1/3], [0]])),
            (np.array([[1 / 3, 0], [0, 1 / 3]]), np.array([[2/3], [0]])),
            (np.array([[1 / 3, 0], [0, 1 / 3]]), np.array([[0], [1/3]])),
            (np.array([[1 / 3, 0], [0, 1 / 3]]), np.array([[2/3], [1/3]])),
            (np.array([[1 / 3, 0], [0, 1 / 3]]), np.array([[0], [2/3]])),
            (np.array([[1 / 3, 0], [0, 1 / 3]]), np.array([[1/3], [2/3]])),
            (np.array([[1 / 3, 0], [0, 1 / 3]]), np.array([[2/3], [2/3]]))
        ]

        super().__init__(transformation_tuples_list)