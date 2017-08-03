import unittest

import routing


class LinkTests(unittest.TestCase):

    def test_Link_creation_Success_When_defaults_used(self):
        link = routing.Link("1", "n1", "n2")
        self.assertEqual(link.link_id, "1", "Link id not set")
        self.assertEqual(link.start_node_id, "n1", "Start node not set")
        self.assertEqual(link.end_node_id, "n2", "End node not set")
        self.assertIsNone(link.metadata, "Metadata contains value")

    def test_Link_creation_metadata_Success_When_defaults_used(self):
        link = routing.Link("1", "n1", "n2", {})
        self.assertEqual(link.link_id, "1", "Link id not set")
        self.assertEqual(link.start_node_id, "n1", "Start node not set")
        self.assertEqual(link.end_node_id, "n2", "End node not set")
        self.assertDictEqual(link.metadata, {}, "Metadata contains value")

    def test_Link_creation_Throws_type_error_When_wrong_metadata_type(self):
        with self.assertRaises(TypeError):
            routing.Link("1", 1, 1, "wrong")


