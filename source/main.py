#!/usr/bin/python
from __future__ import print_function
import pde
import plots


def migrate():
    initial_state = (0., 0., 0.)
    field = pde.get_field(initial_state)
    plots.plot_interpolant(field)


def test():
    migrate()


if __name__ == "__main__":
    test()
