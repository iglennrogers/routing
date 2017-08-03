import math


infinity_cost = 999  # float("inf")


class Node:
    def __init__(self, node_id, coords=None, metadata: dict = None):
        if coords and not (isinstance(coords, tuple) or isinstance(coords, list)):
            raise TypeError("Coords not a recognised form")
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Metadata is not a dictionary")
        self.node_id = node_id
        self.coords = coords
        self.metadata = metadata

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.node_id == other.node_id

    def __hash__(self):
        return hash(self.node_id)

    def __repr__(self):
        return "Node(id={0}, coords={1}, metadata={2})".format(self.node_id, self.coords, self.metadata)


class Link:
    def __init__(self, link_id, start_node_id, end_node_id, metadata: dict = None):
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Metadata is not a dictionary")
        self.link_id = link_id
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.metadata = metadata

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.link_id == other.link_id

    def __hash__(self):
        return hash(self.link_id)

    def __repr__(self):
        return "Link(id={0}, start node={1}, end node={2}, metadata={3})".format(
            self.link_id, self.start_node_id, self.end_node_id, self.metadata)


def distance(node1: Node, node2: Node):
    coords1 = node1.coords
    coords2 = node2.coords
    if not (coords1 and coords2):
        raise ValueError("Coords are null")
    if type(coords1) != type(coords2):
        raise TypeError("Coords do not share same types")
    if len(coords1) != len(coords2):
        raise TypeError("Coords do not share same types")
    length2 = 0
    for p1, p2 in zip(coords1, coords2):
        length2 += (p1 - p2)*(p1 - p2)
    return math.sqrt(length2)


def manhattan_distance(node1: Node, node2: Node):
    coords1 = node1.coords
    coords2 = node2.coords
    if not (coords1 and coords2):
        raise ValueError("Coords are null")
    if type(coords1) != type(coords2):
        raise TypeError("Coords do not share same types")
    if len(coords1) != len(coords2):
        raise TypeError("Coords do not share same types")
    length = 0
    for p1, p2 in zip(coords1, coords2):
        length += abs(p1 - p2)
    return length


class Network:
    def __init__(self):
        self.start_location = None
        self.lowest_cost = {}  # key = node, value = (cost, previous_link)
        self.visited = set()  # key = node

    def initialise_run(self):
        self.start_location = None
        self.lowest_cost.clear()
        self.visited.clear()

    def run(self, start_location: Node):
        self.initialise_run()
        self.start_location = start_location
        self.lowest_cost[self.start_location] = 0, None
        #
        loose_ends = [(0, start_location)]
        #
        while len(loose_ends) > 0:
            loose_ends.sort(key=lambda x: x[0])
            current_node = loose_ends[0][1]
            del loose_ends[0]
            if current_node in self.visited:
                continue
            #
            current_cost, prev_link = self.lowest_cost[current_node]
            self.visited.add(current_node)
            #
            links = self.get_links_attached(current_node)
            for link in links:
                node_cost = self.junction_cost(prev_link, current_node, link)
                link_cost = self.link_cost(link, current_node)
                total_cost = current_cost + node_cost + link_cost
                #
                other = self.get_other_node(link, current_node)
                assert other != current_node
                if other in self.lowest_cost:
                    last_cost, _ = self.lowest_cost[other]
                else:
                    last_cost = infinity_cost
                if total_cost < last_cost:
                    self.lowest_cost[other] = total_cost, link
                    loose_ends.append((total_cost, other))
                elif last_cost != infinity_cost:
                    loose_ends.append((last_cost, other))

    def get_cost(self, node: Node):
        if node in self.lowest_cost:
            return self.lowest_cost[node][0]
        else:
            return infinity_cost

    def get_previous_link(self, node: Node):
        if node in self.lowest_cost:
            return self.lowest_cost[node][1]
        else:
            return None

    def get_path(self, end_node: Node):
        path = []
        if end_node in self.lowest_cost:
            curr = end_node
            while curr != self.start_location:
                path.append(curr)
                _, prev = self.lowest_cost[curr]
                curr = self.get_other_node(prev, curr)
            path.append(curr)
        return [x for x in reversed(path)]

    def get_path_ids(self, end_node: Node):
        path = self.get_path(end_node)
        return [n.node_id for n in path]

    def get_links_attached(self, node: Node):
        raise NotImplementedError

    def get_other_node(self, link: Link, start_node: Node):
        raise NotImplementedError

    def junction_cost(self, link_prev: Link, middle_node: Node, link_next: Link):
        raise NotImplementedError

    def link_cost(self, link: Link, start_node: Node):
        raise NotImplementedError
