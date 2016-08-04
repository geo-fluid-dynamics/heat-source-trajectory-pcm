#!/usr/bin/python
from __future__ import print_function
import matplotlib.pyplot as plt
import field
import trajectory


def test():
    field.test()
    plt.show()
    trajectory.migrate()
    plt.show()

if __name__ == "__main__":
    test()
