import unittest

import routing


class NodeTests(unittest.TestCase):

    def test_Node_creation_Success_When_defaults_used(self):
        start = routing.Node("1", (4, 2))
        self.assertEqual(start.node_id, "1", "Node id not set")
        self.assertTupleEqual(start.coords, (4, 2), "Coords not set")
        self.assertIsNone(start.metadata, "Metadata contains value")

    def test_Node_creation_Throws_type_error_When_wrong_coord_type(self):
        with self.assertRaises(TypeError):
            routing.Node("1", "wrong")

    def test_Node_creation_Throws_type_error_When_wrong_metadata_type(self):
        with self.assertRaises(TypeError):
            routing.Node("1", (0,0), "wrong")

    def test_Node_creation_metadata_Success_When_defaults_used(self):
        start = routing.Node("1", (4, 2), {})
        self.assertEqual(start.node_id, "1", "Node id not set")
        self.assertTupleEqual(start.coords, (4, 2), "Coords not set")
        self.assertDictEqual(start.metadata, {}, "Metadata does not contain value")

    def test_Node_creation_Success_for_no_coordinates(self):
        start = routing.Node("1")
        self.assertEqual(start.node_id, "1", "Node id not set")
        self.assertIsNone(start.coords, "Coords not set")
        self.assertIsNone(start.metadata, "Metadata contains value")

    def test_Node_creation_Success_for_1D_coordinates(self):
        start = routing.Node("1", (4,))
        self.assertEqual(start.node_id, "1", "Node id not set")
        self.assertTupleEqual(start.coords, (4,), "Coords not set")
        self.assertIsNone(start.metadata, "Metadata contains value")

    def test_Node_creation_Success_for_3D_coordinates(self):
        start = routing.Node("1", (4, 3, 2))
        self.assertEqual(start.node_id, "1", "Node id not set")
        self.assertTupleEqual(start.coords, (4, 3, 2), "Coords not set")
        self.assertIsNone(start.metadata, "Metadata contains value")


