from mung_manager.sum import custom_sum


def test_sum():
    assert custom_sum(1, 2) == 3
    assert custom_sum(1, 3) == 4
