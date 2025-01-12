from nietzsche.space import Space
from nietzsche.utils import Dimension

class TestSpace:

    def test_init(self):
        space = Space(dimension=Dimension.D.value, geometry="Euclidean")
        assert len(space.setup()) == 1
