from fractal.generation import IterativeTransformer
import numpy as np
import math

class SimpleFern(IterativeTransformer):
    def __init__(self):
        branch_angle = 0.6 * math.pi
        branch_scale = 0.25
        stem_angle = -0.06 * math.pi
        stem_scale = 0.9
        collapse_scale = 0.20
        transformation_tuples_list = [
            (np.array([[0, 0], [0, collapse_scale]]), np.array([[0], [0]])),
            (branch_scale * np.array([[math.cos(branch_angle), math.sin(branch_angle)], [-math.sin(branch_angle), math.cos(branch_angle)]]), np.array([[0], [0.667]])),
            (np.array([[-branch_scale, 0], [0, branch_scale]]) @ np.array(
                [[math.cos(branch_angle), math.sin(branch_angle)], [-math.sin(branch_angle), math.cos(branch_angle)]]),
             np.array([[0], [0.333]])),
            (stem_scale * np.array(
                [[math.cos(stem_angle), math.sin(stem_angle)], [-math.sin(stem_angle), math.cos(stem_angle)]]),
             np.array([[0], [1]])),
        ]

        super().__init__(transformation_tuples_list, corresponding_probabilities=[0.02, 0.09, 0.09, 0.8])