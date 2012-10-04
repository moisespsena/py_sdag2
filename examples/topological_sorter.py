'''
Created on Oct 3, 2012

@author: Moises P. Sena
'''
from sdag2 import DAG

dag = DAG()
a = dag.add("A")
b = dag.add("B")
c = dag.add("C")
d = dag.add("D")

dag.add_edge(c, a)
dag.add_edge(a, b)
dag.add_edge(b, d)
dag.add_edge(c, d)

rs = dag.topologicaly()
# Order is: C --> A --> B --> D
print("Order is: %s" % (" --> ".join(rs)))

assert rs.index("C") < rs.index("A")
assert rs.index("A") < rs.index("B")
assert rs.index("B") < rs.index("D")
assert rs.index("C") < rs.index("D")