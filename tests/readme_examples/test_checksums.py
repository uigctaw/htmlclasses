from .generate_checksums import calculate_checksums, read_checksums


def test_calculated_checksums_are_same_as_saved_checksums():
    calculated = calculate_checksums()
    read = read_checksums()
    difference = [
        name
        for name in set(calculated) | set(read)
        if calculated.get(name) != read.get(name)
    ]
    assert calculated
    assert not difference, difference
