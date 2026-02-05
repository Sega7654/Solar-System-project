import pytest
from project import date_input_check_1, Planets_input_fun_1, asteroid_check_1



def test_date_input_check_1():
    assert date_input_check_1("asd") == False
    assert date_input_check_1("191239") == False
    assert date_input_check_1("1999-01-42") == False
    assert date_input_check_1("1999-01-01") == True

def test_asteroid_check_1():
    assert asteroid_check_1(" Y ") == "y"
    assert asteroid_check_1("N ") == "n"
    with pytest.raises(ValueError):
        asteroid_check_1("Yes")
    with pytest.raises(ValueError):
        asteroid_check_1("asd")
    with pytest.raises(ValueError):
        asteroid_check_1("123")

def test_Planets_input_fun_1():
    planets_order = ["Mercury", "Venus", "Earth", "Mars", 
                "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    assert Planets_input_fun_1(" eaRtH   ") == ["Earth"]
    assert Planets_input_fun_1("earth, mars") == ["Earth", "Mars"]
    assert Planets_input_fun_1("mars,earth") == ["Earth", "Mars"]
    assert Planets_input_fun_1("  fULl   ") == planets_order
    with pytest.raises(ValueError):
        Planets_input_fun_1("earth, full")
    with pytest.raises(ValueError):
        Planets_input_fun_1("fULl, earTh")
    with pytest.raises(ValueError):
        Planets_input_fun_1("earth, 123")
    with pytest.raises(ValueError):
        Planets_input_fun_1("earth, mrs")
    with pytest.raises(ValueError):
        Planets_input_fun_1("erth")