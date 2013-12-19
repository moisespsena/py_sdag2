'''
Created on Oct 1, 2012

@author: Moises P. Sena
'''
NOT_VISITED = 0
VISITING = 1
VISITED = 2

import sys
_range = xrange if sys.version_info < (3,) else range

class CycleDetectedException(Exception):
    def __init__(self, value, cycle):
        self.cycle = cycle
        self.value = "%s: { %s }" % (value, " --> ".join(cycle),)

    def __str__(self):
        return self.value

class CycleDetector:
    def __init__(self, dag):
        self.dag = dag

    def _has(self):
        verticies = self.dag.verticies
        state_map = dict()
        retValue = []

        for vertex in verticies:
            if self.not_visited(vertex, state_map):
                retValue = self.introduces_cycle(vertex, state_map)

                if retValue == None:
                    break

    has = property(lambda self: self._has())

    def is_not_visited(self, vertex, state_map):
        if not vertex in state_map:
            return True

        state = state_map[vertex]

        if state == NOT_VISITED:
            return True

        return False

    def is_visiting(self, vertex, state_map):
        if not vertex in state_map:
            return False

        state = state_map[vertex]

        if state == VISITING:
            return True

        return False

    def introduces_cycle(self, vertex, state_map=None):
        if state_map == None:
            state_map = dict()

        cycle_stack = []
        has_cycle = self.dfs_visit(vertex, cycle_stack, state_map)

        if has_cycle:
            first_key = cycle_stack[0]
            cycle = [first_key]

            for i in _range(1, len(cycle_stack)):
                key = cycle_stack[i]

                if first_key != key:
                    cycle.append(key)
                else:
                    cycle.append(key)
                    break

            return cycle
        return None

    def dfs_visit(self, vertex, cycle, state_map):
        cycle.insert(0, vertex)

        state_map[ vertex ] = VISITING

        verticies = vertex.children

        for v in verticies:
            if self.is_not_visited(v, state_map):
                hasCycle = self.dfs_visit(v, cycle, state_map)

                if hasCycle:
                    return True

            elif self.is_visiting(v, state_map):
                cycle.insert(0, v)

                return True

        state_map[vertex] = VISITED

        del cycle[0]

        return False

class Vertex:
    def __init__(self, key):
        self.key = key
        self.children = set()
        self.parents = set()

    def add_edge_to(self, vertex):
        self.children.add(vertex)

    def rm_edge_to(self, vertex):
        self.children.remove(vertex)

    def add_edge_from(self, vertex):
        self.parents.add(vertex)

    def rm_edge_from(self, vertex):
        self.parents.remove(vertex)

    def _child_keys(self):
        keys = []

        for lbl in self.children:
            keys.append(lbl)

        return keys

    child_keys = property(lambda self: self._child_keys())

    def _parent_keys(self):
        keys = []

        for lbl in self.parents:
            keys.append(lbl)

        return keys

    parent_keys = property(lambda self: self._parent_keys())

    def _is_leaf(self):
        return len(self.children) == 0

    is_leaf = property(lambda self: self._is_leaf())

    def _is_root(self):
        return len(self.parents) == 0

    is_root = property(lambda self: self._is_root())

    def _is_connected(self):
        if self.is_leaf() or self.is_root():
            return True
        return False

    is_connected = property(lambda self: self._is_connected())

    def __str__(self):
        return "Vertex{%s}" % (self.key,)

    def __eq__(self, other):
        if isinstance(other, Vertex):
            if(self.key == other.key):
                return True
        else:
            return self.key == other

    def __nq__(self, other):
        if isinstance(other, Vertex):
            if(self.key == other.key):
                return False
        return True

    def __hash__(self):
        return self.key.__hash__()

class _node:
    def __init__(self):
        self.data = None
        self.next = None

class _LinkedList:
    def __init__(self):
        self.head = None
        self.current = None

    def add_on_head(self, data):
        new_node = _node() # create a new node
        new_node.data = data
        new_node.next = self.head # link the new node to the 'previous' node.
        self.head = new_node #  set the current node to the new one.

    def reset(self):
        self.current = self.head

    def next(self):
        if self.current:
            self.current = self.current.next

    def data(self):
        if self.current:
            return self.current.data

        return None

    def __str__(self):
        data_list = []
        node = self.head

        while node:
            data_list.append(str(node.data))
            node = node.next

        return "LinkedList{" + ", ".join(data_list) + "}"

    def to_gen(self):
        node = self.head

        if node:
            yield node.data.key

        while node:
            node = node.next
            if node:
                yield node.data.key

    def to_list(self):
        data_list = []
        node = self.head

        while node:
            data_list.append(node.data.key)
            node = node.next

        return data_list

    def __iter__(self):
        return self.to_gen()

def _sort_topologicaly(source, gen=False):
    if isinstance(source, Vertex):
        rs = _sort_vertex(source, gen=gen)
    elif isinstance(source, DAG):
        rs = _dfs(source, gen=gen);

    return rs

def _sort_vertex(vertex, gen=False):
    lis = _LinkedList()
    state_map = dict()
    _dfs_visit(vertex, state_map, lis)

    if gen:
        return lis.to_gen()
    else:
        return lis.to_list()

def _dfs(graph, gen=False):
    lis = _LinkedList()
    state_map = dict()

    for vertex in graph.verticies:
        if _is_not_visited(vertex, state_map):
            _dfs_visit(vertex, state_map, lis)

    if gen:
        return lis.to_gen()
    else:
        return lis.to_list()

def _is_not_visited(vertex, state_map):
    if not vertex in state_map:
        return True

    state = state_map[ vertex ]

    return NOT_VISITED == state

def _dfs_visit(vertex, state_map, lis):
    state_map[vertex] = VISITING

    verticies = vertex.children;

    for v in verticies:
        if _is_not_visited(v, state_map):
            _dfs_visit(v, state_map, lis)

    state_map[vertex] = VISITED;
    lis.add_on_head(vertex);

class DAG:
    def __init__(self):
        self.map = dict()

    def _get_keys(self):
        return self.map.keys()

    def __add__(self, key):
        self.add(key)
        return self

    def add(self, key):
        if key in self.map:
            return self.map[key]
        else:
            ret = Vertex(key)
            self.map[key] = ret
            return ret

    def remove(self, key):
        vertex = self.add(key)

        for c in vertex.children:
            c.parents.remove(vertex)

    def vertex(self, key):
        ret = None

        if key in self.map:
            ret = self.map[key]

        return ret

    def add_edge(self, from_vertex, to_vertex):
        from_vertex = self.add(from_vertex)
        to_vertex = self.add(to_vertex)

        from_vertex.add_edge_to(to_vertex)
        to_vertex.add_edge_from(from_vertex)

        detector = CycleDetector(self)
        cycle = detector.introduces_cycle(to_vertex)

        if cycle != None:
            self.rm_edge(from_vertex, to_vertex)

            msg = "Edge between '" + str(from_vertex) + "' and '" + str(to_vertex) + "' introduces to cycle in the graph"

            raise CycleDetectedException(msg, [v.key for v in cycle])

    def rm_edge(self, from_vertex, to_vertex):
        from_vertex.rm_edge_to(to_vertex)
        to_vertex.rm_edge_from(from_vertex)

    def get_verticies(self):
        for k in self.map:
            yield self.map[k]

    verticies = property(lambda self: self.get_verticies())

    def __str__(self):
        verticies = []

        if len(self.map) == 0:
            return "DAG{}"

        for k in self.map:
            verticies.append(k)

        return "DAG{'" + "', '".join(verticies) + "'}"

    def topologicaly(self, gen=False):
        return _sort_topologicaly(self, gen=gen)
