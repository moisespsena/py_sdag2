'''
Created on Oct 2, 2012

@author: Moises P. Sena
'''
import unittest
from py_sdag2 import DAG, CycleDetectedException

class DAGTest(unittest.TestCase):    
    def test_simple(self):
        '''
        Tests the verticles order in:
        
        C --> A --> B --> D
        '''
        
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
        
        self.assertTrue(rs.index("C") < rs.index("A"))
        self.assertTrue(rs.index("A") < rs.index("B"))
        self.assertTrue(rs.index("B") < rs.index("D"))
        self.assertTrue(rs.index("C") < rs.index("D"))
        
    def test_cicle_detect(self):
        '''
        Tests the verticles order in:
        
        C --> A --> B --> D -> C
        '''
        
        dag = DAG()
        a = dag.add("A")
        b = dag.add("B")
        c = dag.add("C")
        d = dag.add("D")
        
        dag.add_edge(c, a)
        dag.add_edge(a, b)
        dag.add_edge(b, d)
        dag.add_edge(c, d)
        
        try:
            # add cicle at A --> C --> A
            dag.add_edge(a, c)
            raise Exception("Cycle not detected")
        except CycleDetectedException: pass

def main():
    unittest.main()
    
if __name__ == "__main__":
    main()
