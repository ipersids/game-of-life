from project import get_pattern, get_neighbours, run_evolution
import pytest

def test_get_pattern():
    assert get_pattern(name="Glader") == {'Glader': [(1, 1), (2, 2), (3, 2), (1, 3), (2, 3)]}
    assert get_pattern(name="Blinker") == {"Blinker": [(1, 1), (2, 1), (3, 1)]}
    assert get_pattern(name="Toad") == {"Toad": [(1, 1), (2, 1), (3, 1), (2, 2), (3, 2), (4, 2)]}

    with pytest.raises(KeyError):
        get_pattern(name="name")


def test_get_neighbours():
    """
    neighbr = [
        (-1, -1), (-1, 0), (-1, 1), 
        (0, -1), (0, 1), 
        (1, -1), (1, 0), (1, 1)
    ]
    """
    pattern_1 = get_pattern(name="Glader")
    assert list(get_neighbours(pattern_1["Glader"]).keys()) == [
            (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), 
            (2, 1), (2, 2), (1, 1), (1, 3), (2, 3), (3, 1), 
            (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (0, 3), 
            (0, 4), (1, 4), (2, 4), (3, 4)
        ]
    
    pattern_2 = get_pattern(name="Blinker")
    assert list(get_neighbours(pattern_2["Blinker"]).keys())[:4] == [
            (0, 0), (0, 1), (0, 2), (1, 0)
        ]
    
    pattern_3 = get_pattern(name="Toad")
    assert list(get_neighbours(pattern_3["Toad"]).keys())[:4] == [
            (0, 0), (0, 1), (0, 2), (1, 0)
        ]
    

def test_run_evolution():
    # {'Blinker': [(1, 1), (2, 1), (3, 1)]})
    pattern_1 = get_pattern(name="Blinker")
    neighbours_1 = get_neighbours(pattern_1["Blinker"])
    assert run_evolution(pattern_1["Blinker"], neighbours_1, 100, 100) == [(2, 0), (2, 1), (2, 2)]

    pattern_after_evo = run_evolution(pattern_1["Blinker"], neighbours_1, 100, 100)
    neighbours_after_evo = get_neighbours(pattern_after_evo)
    assert run_evolution(pattern_after_evo, neighbours_after_evo, 100, 100) == [(1, 1), (2, 1), (3, 1)]

    # {'Glader': [(1, 1), (2, 2), (3, 2), (1, 3), (2, 3)]})
    pattern_1 = get_pattern(name="Glader")
    neighbours_1 = get_neighbours(pattern_1["Glader"])
    assert run_evolution(pattern_1["Glader"], neighbours_1, 100, 100) == [(2, 1), (1, 3), (2, 3), (3, 2), (3, 3)]