from nietzsche.utils import Dimension

class TestDimension:

    def test_dimension(self):
        assert Dimension.D.value == 1
        assert Dimension.DD.value == 2
        assert Dimension.DDD.value == 3

