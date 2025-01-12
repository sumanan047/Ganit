from nietzsche.space import Space

class TestSpace:

    def test_init(self):
        space = Space()
        assert space.ndim == 3
        assert space.shape == (100,100,100)

    def test_set(self):
        space = Space()
        s = space.setup()
        assert s.shape == (100,100,100)

        s = space.setup(shape=(200,100,50))
        assert s.shape == (200,100,50)
