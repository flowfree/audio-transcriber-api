from .tasks import square_root


def test_square_root():
    assert square_root(4) == 2.0
    assert square_root(9) == 3.0
    assert square_root(2) == 1.4142
