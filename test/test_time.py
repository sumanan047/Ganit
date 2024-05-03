import numpy as np
import pytest
from nietzsche.time_ import Time


class TestTime:

    def test_init(self):
        time = Time()
        assert not time.reletivistic

    def test_set(self):
        time = Time()
        t = time.set()
        assert t[0] == 0.0
        assert t[-1] == 10.0
        assert len(t) == 101

        t = time.set(start=1.0, step=200, dt=0.05)
        assert t[0] == 1.0
        assert t[-1] == 11.0
        assert len(t) == 201
