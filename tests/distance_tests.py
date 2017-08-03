import math
import unittest
import routing


class DistanceTests(unittest.TestCase):

    def test_Distance_Correct_value_When_1D_coords_used(self):
        start = routing.Node(1, (1,))
        end = routing.Node(2, (3,))
        self.assertEqual(routing.distance(start, end), 2, msg="Incorrect distance between nodes")

    def test_Distance_Correct_value_When_2D_coords_used(self):
        start = routing.Node(1, (1, 1))
        end = routing.Node(2, (3, 3))
        self.assertAlmostEqual(routing.distance(start, end), math.sqrt(8), msg="Incorrect distance between nodes")

    def test_Distance_Correct_value_When_3D_coords_used(self):
        start = routing.Node(1, (1, 1, 1))
        end = routing.Node(2, (3, 3, 3))
        self.assertAlmostEqual(routing.distance(start, end), math.sqrt(12), msg="Incorrect distance between nodes")

    def test_Distance_Throw_value_error_When_no_coords_used(self):
        with self.assertRaises(ValueError):
            start = routing.Node(1)
            end = routing.Node(2, (3,))
            routing.distance(start, end)
        with self.assertRaises(ValueError):
            start = routing.Node(1, (4, 7))
            end = routing.Node(2)
            routing.distance(start, end)

    def test_Distance_Throws_type_error_When_mixed_coords_dimension_used(self):
        with self.assertRaises(TypeError):
            start = routing.Node(1, (1,))
            end = routing.Node(2, (3, 2))
            routing.distance(start, end)

    def test_Distance_Throws_type_error_When_mixed_coords_types_used(self):
        with self.assertRaises(TypeError):
            start = routing.Node(1, (1, 2))
            end = routing.Node(2, [3, 2])
            routing.distance(start, end)

    def test_Manhattan_distance_Correct_value_When_1D_coords_used(self):
        start = routing.Node(1, (1,))
        end = routing.Node(2, (3,))
        self.assertEqual(routing.manhattan_distance(start, end), 2, msg="Incorrect distance between nodes")

    def test_Manhattan_distance_Correct_value_When_2D_coords_used(self):
        start = routing.Node(1, (1, 1))
        end = routing.Node(2, (3, 3))
        self.assertAlmostEqual(routing.manhattan_distance(start, end), 4, msg="Incorrect distance between nodes")

    def test_Manhattan_distance_Correct_value_When_3D_coords_used(self):
        start = routing.Node(1, (1, 1, 1))
        end = routing.Node(2, (3, 3, 3))
        self.assertAlmostEqual(routing.manhattan_distance(start, end), 6, msg="Incorrect distance between nodes")

    def test_Manhattan_distance_Throws_value_error_When_no_coords_used(self):
        with self.assertRaises(ValueError):
            start = routing.Node(1)
            end = routing.Node(2, (3,))
            routing.manhattan_distance(start, end)
        with self.assertRaises(ValueError):
            start = routing.Node(1, (4, 7))
            end = routing.Node(2)
            routing.manhattan_distance(start, end)

    def test_Manhattan_distance_Throws_type_error_When_mixed_coords_dimension_used(self):
        with self.assertRaises(TypeError):
            start = routing.Node(1, (1,))
            end = routing.Node(2, (3, 2))
            routing.manhattan_distance(start, end)

    def test_Manhattan_distance_Throws_type_error_When_mixed_coords_types_used(self):
        with self.assertRaises(TypeError):
            start = routing.Node(1, (1, 2))
            end = routing.Node(2, [3, 2])
            routing.manhattan_distance(start, end)

