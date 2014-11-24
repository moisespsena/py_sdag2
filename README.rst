============================================
SDAG2 - Python Simple Directed Acyclic Graph
============================================

The Python Simple Directed Graph whith Cicle Detector and TopoloGical sorter utilities.

Project Home Page
=================

This project was be hosted on `Github`_.

Authors
-------

- `Moises P. Sena`_

Install
-------

Install it using the `Python PIP Project`_.

.. code:: bash

    pip install sdag2


Scripts
-------

tsort.py
~~~~~~~~

Sources from Standard Input:

.. code:: bash

    echo -e 'C A\nA B\nB D\nC D' | tsort.py


Sources from another file:

.. code:: bash

    echo -e 'C A\nA B\nB D\nC D' > verticies.txt
    tsort.py verticies.txt

More Options:

.. code:: bash

    tsort.py --help
    Usage: tsort.py [options] [FILE [OUT_FILE]]

    Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  With no FILE, or when FILE is -, read standard input.
      -o OUT_FILE, --out-file=OUT_FILE
                            Write result to OUT_FILE, default is standard output.
      -s SEP, --separator=SEP
                            Items separator, default is \s regex.
      -q QUIT_SEQ, --quit-sequence=QUIT_SEQ
                            Stop read FILE where line equals QUIT_SEQ, default is
                            :quit.


Tests
-----

.. code:: python

    import unittest
    from sdag2 import DAG, CycleDetectedException

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

.. _Moises P. Sena: http://moisespsena.com
.. _Github: https://github.com/moisespsena/py_sdag
.. _Python PIP Project: https://pypi.python.org/pypi/pip