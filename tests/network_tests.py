import unittest

import routing


class NetworkTests(unittest.TestCase):

    class NonNetwork(routing.Network):
        def __init__(self):
            super().__init__()

        def get_links_attached(self, node: routing.Node):
            return []

        def get_other_node(self, link: routing.Link, start_node: routing.Node):
            raise NotImplementedError

        def junction_cost(self, link_prev_id, middle_node_id, link_next_id):
            raise NotImplementedError

        def link_cost(self, link, start_node_id):
            raise NotImplementedError

    class SimpleNetwork(routing.Network):
        def __init__(self, nodes, links):
            super().__init__()
            self.nodes = nodes
            self.links = links

        def get_links_attached(self, node: routing.Node):
            links = []
            for link in self.links.values():
                if node.node_id in [link.start_node_id, link.end_node_id]:
                    links.append(link)
            return links

        def get_other_node(self, link: routing.Link, start_node: routing.Node):
            if link.start_node_id == start_node.node_id:
                return self.nodes[link.end_node_id]
            elif link.end_node_id == start_node.node_id:
                return self.nodes[link.start_node_id]
            else:
                raise ValueError("Node not connected to link")

        def junction_cost(self, link_prev: routing.Link, middle_node: routing.Node, link_next: routing.Link):
            return 0

        def link_cost(self, link: routing.Link, start_node: routing.Node):
            return routing.distance(self.nodes[link.start_node_id], self.nodes[link.end_node_id])

    def test_Non_network_Values_correct_Network_single_point(self):
        nodes = {1: routing.Node(1, (0,))}
        network = NetworkTests.NonNetwork()
        network.run(nodes[1])
        cost, prev = network.get_cost(nodes[1]), network.get_previous_link(nodes[1])
        path = network.get_path_ids(nodes[1])
        self.assertEqual(cost, 0, "Cost to self is not zero")
        self.assertIsNone(prev, "Node has a previous link")
        self.assertListEqual(path, [1], "Wrong shortest path")

    def test_Non_network_Values_correct_Network_unconnected_point(self):
        nodes = {1: routing.Node(1, (0,)), 2: routing.Node(2, (1,))}
        network = NetworkTests.NonNetwork()
        network.run(nodes[1])
        cost, prev = network.get_cost(nodes[2]), network.get_previous_link(nodes[2])
        path = network.get_path_ids(nodes[2])
        self.assertEqual(cost, routing.infinity_cost, "Node is connected to network")
        self.assertListEqual(path, [], "Wrong shortest path")

    def test_Simple_network_Values_correct_Network_points(self):
        nodes = {1: routing.Node(1, (0,)), 2: routing.Node(2, (1,)), 3: routing.Node(3, (9,))}
        links = {1: routing.Link(1, 1, 2)}
        network = NetworkTests.SimpleNetwork(nodes, links)
        network.run(nodes[1])
        #
        cost, prev = network.get_cost(nodes[1]), network.get_previous_link(nodes[1])
        path = network.get_path_ids(nodes[1])
        self.assertEqual(cost, 0, "Cost to start is not zero")
        self.assertIsNone(prev, "Node has a previous link")
        self.assertListEqual(path, [1], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[2]), network.get_previous_link(nodes[2])
        path = network.get_path_ids(nodes[2])
        self.assertEqual(cost, 1, "Cost to end is not 1")
        self.assertEqual(prev, links[1], "Node has incorrect route")
        self.assertListEqual(path, [1, 2], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[3]), network.get_previous_link(nodes[3])
        path = network.get_path_ids(nodes[3])
        self.assertEqual(cost, routing.infinity_cost, "Node is connected to network")
        self.assertListEqual(path, [], "Wrong shortest path")

    def test_Simple_network_Values_correct_Network_branched(self):
        nodes = {1: routing.Node(1, (0, 0)), 2: routing.Node(2, (1, 0)), 3: routing.Node(3, (0, 1)),
                 4: routing.Node(4, (0, -1)), 5: routing.Node(5, (-1, 0))}
        links = {1: routing.Link(1, 1, 2), 2: routing.Link(2, 1, 3), 3: routing.Link(3, 1, 4),
                 4: routing.Link(4, 1, 5), }
        network = NetworkTests.SimpleNetwork(nodes, links)
        network.run(nodes[1])
        #
        cost, prev = network.get_cost(nodes[1]), network.get_previous_link(nodes[1])
        path = network.get_path_ids(nodes[1])
        self.assertEqual(cost, 0, "Cost to start is not zero")
        self.assertIsNone(prev, "Node has a previous link")
        self.assertListEqual(path, [1], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[2]), network.get_previous_link(nodes[2])
        path = network.get_path_ids(nodes[2])
        self.assertEqual(cost, 1, "Cost to 2 is not 1")
        self.assertEqual(prev, links[1], "Node has incorrect route")
        self.assertListEqual(path, [1, 2], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[3]), network.get_previous_link(nodes[3])
        path = network.get_path_ids(nodes[3])
        self.assertEqual(cost, 1, "Cost to 3 is not 1")
        self.assertEqual(prev, links[2], "Node has incorrect route")
        self.assertListEqual(path, [1, 3], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[4]), network.get_previous_link(nodes[4])
        path = network.get_path_ids(nodes[4])
        self.assertEqual(cost, 1, "Cost to 4 is not 1")
        self.assertEqual(prev, links[3], "Node has incorrect route")
        self.assertListEqual(path, [1, 4], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[5]), network.get_previous_link(nodes[5])
        path = network.get_path_ids(nodes[5])
        self.assertEqual(cost, 1, "Cost to 5 is not 1")
        self.assertEqual(prev, links[4], "Node has incorrect route")
        self.assertListEqual(path, [1, 5], "Wrong shortest path")

    def test_Simple_network_Values_correct_Network_cycle(self):
        nodes = {1: routing.Node(1, (0, 0)), 2: routing.Node(2, (1, 0)), 3: routing.Node(3, (3, 4))}
        links = {1: routing.Link(1, 1, 2), 2: routing.Link(2, 2, 3), 3: routing.Link(3, 1, 3)}
        network = NetworkTests.SimpleNetwork(nodes, links)
        network.run(nodes[1])
        #
        cost, prev = network.get_cost(nodes[1]), network.get_previous_link(nodes[1])
        path = network.get_path_ids(nodes[1])
        self.assertEqual(cost, 0, "Cost to start is not zero")
        self.assertIsNone(prev, "Node has a previous link")
        self.assertListEqual(path, [1], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[2]), network.get_previous_link(nodes[2])
        path = network.get_path_ids(nodes[2])
        self.assertEqual(cost, 1, "Cost to 2 is not 1")
        self.assertEqual(prev, links[1], "Node has incorrect route")
        self.assertListEqual(path, [1, 2], "Wrong shortest path")
        #
        cost, prev = network.get_cost(nodes[3]), network.get_previous_link(nodes[3])
        path = network.get_path_ids(nodes[3])
        self.assertEqual(cost, 5, "Cost to 3 is not 5")
        self.assertEqual(prev, links[3], "Node has incorrect route")
        self.assertListEqual(path, [1, 3], "Wrong shortest path")

    class ComplexNetwork(routing.Network):
        def __init__(self, nodes, links):
            super().__init__()
            self.nodes = nodes
            self.links = links

        def get_links_attached(self, node: routing.Node):
            links = []
            for link in self.links.values():
                if node.node_id in [link.start_node_id, link.end_node_id]:
                    links.append(link)
            return links

        def get_other_node(self, link: routing.Link, start_node: routing.Node):
            if link.start_node_id == start_node.node_id:
                return self.nodes[link.end_node_id]
            elif link.end_node_id == start_node.node_id:
                return self.nodes[link.start_node_id]
            else:
                raise ValueError("Node not connected to link")

        def junction_cost(self, link_prev: routing.Link, middle_node: routing.Node, link_next: routing.Link):
            if link_prev and link_prev.metadata:
                if "banned turn" in link_prev.metadata:
                    banned_link_id = link_prev.metadata["banned turn"]
                    if link_next.link_id == banned_link_id:
                        return routing.infinity_cost
            if link_next and link_next.metadata:
                if "no entry" in link_next.metadata:
                    return routing.infinity_cost
            if middle_node and middle_node.metadata:
                if "traffic lights" in middle_node.metadata:
                    return middle_node.metadata["traffic lights"]
            return 0

        def link_cost(self, link: routing.Link, start_node: routing.Node):
            return 10

    def test_Complex_network_Values_correct_Traffic_lights(self):
        nodes = {1: routing.Node(1), 2: routing.Node(2, metadata={"traffic lights": 5}), 3: routing.Node(3)}
        links = {1: routing.Link(1, 1, 2), 2: routing.Link(2, 2, 3)}
        network = NetworkTests.ComplexNetwork(nodes, links)
        network.run(nodes[1])
        cost, prev = network.get_cost(nodes[3]), network.get_previous_link(nodes[3])
        path = network.get_path_ids(nodes[3])
        self.assertEqual(cost, 25, "Cost to target is not correct")
        self.assertEqual(prev, links[2], "Node has wrong previous link")
        self.assertListEqual(path, [1, 2, 3], "Wrong shortest path")

    def test_Complex_network_Values_correct_No_entry(self):
        nodes = {1: routing.Node(1), 2: routing.Node(2), 3: routing.Node(3)}
        links = {1: routing.Link(1, 1, 2), 2: routing.Link(2, 2, 3, {"no entry": True})}
        network = NetworkTests.ComplexNetwork(nodes, links)
        network.run(nodes[1])
        cost, prev = network.get_cost(nodes[3]), network.get_previous_link(nodes[3])
        path = network.get_path_ids(nodes[3])
        self.assertEqual(cost, routing.infinity_cost, "Cost to target is not correct")
        self.assertIsNone(prev, "Node has wrong previous link")
        self.assertListEqual(path, [], "Wrong shortest path")

    def test_Complex_network_Values_correct_Banned_turn(self):
        nodes = {1: routing.Node(1), 2: routing.Node(2), 3: routing.Node(3), 4: routing.Node(4), 5: routing.Node(5)}
        links = {1: routing.Link(1, 1, 2, {"banned turn": 2}), 2: routing.Link(2, 2, 3),
                 3: routing.Link(3, 2, 4), 4: routing.Link(4, 4, 5), 5: routing.Link(5, 5, 3)}
        network = NetworkTests.ComplexNetwork(nodes, links)
        network.run(nodes[1])
        cost, prev = network.get_cost(nodes[3]), network.get_previous_link(nodes[3])
        path = network.get_path_ids(nodes[3])
        self.assertEqual(cost, 40, "Cost to target is not correct")
        self.assertEqual(prev, links[5], "Node has wrong previous link")
        self.assertListEqual(path, [1, 2, 4, 5, 3], "Wrong shortest path")


class ExampleNetworkTests(unittest.TestCase):

    class ExampleNetwork1(routing.Network):

        def __init__(self):
            super().__init__()
            self.graph = {'s': {'u': 10, 'x': 5}, 'u': {'v': 1, 'x': 2}, 'v': {'y': 4},
                          'x': {'u': 3, 'v': 9, 'y': 2}, 'y': {'s': 7, 'v': 6}}

        def get_links_attached(self, node: routing.Node):
            links = self.graph[node.node_id]
            return [routing.Link(node.node_id + k, node.node_id, k) for k in links]

        def get_other_node(self, link: routing.Link, start_node: routing.Node):
            if link.start_node_id == start_node.node_id:
                return routing.Node(link.end_node_id)
            elif link.end_node_id == start_node.node_id:
                return routing.Node(link.start_node_id)
            else:
                raise ValueError("Node not connected to link")

        def junction_cost(self, link_prev: routing.Link, middle_node: routing.Node, link_next: routing.Link):
            return 0

        def link_cost(self, link: routing.Link, start_node: routing.Node):
            cost = self.graph[start_node.node_id][link.end_node_id]
            return cost

    def test_Simple_network_Values_correct_Example_Network(self):
        network = ExampleNetworkTests.ExampleNetwork1()
        network.run(routing.Node('s'))
        #
        cost, prev = network.get_cost(routing.Node('v')), network.get_previous_link(routing.Node('v'))
        path = network.get_path_ids(routing.Node('v'))
        self.assertEqual(cost, 9, "Cost to end is not 9")
        self.assertEqual(prev.link_id, 'uv', "Node has incorrect previous link")
        self.assertListEqual(path, ['s', 'x', 'u', 'v'], "Wrong shortest path")

