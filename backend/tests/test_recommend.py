"""pytest tests for recommend.py"""

from recommend import recommend_meal

def test_recommend_meal_output():
    nutrition = {
        "calories": 850,
        "protein": 25,
        "carbohydrates": 30,
        "fiber": 2,
        "calcium": 150
    }
    result = recommend_meal(nutrition)

    # check if output has 2 items
    assert len(result) == 2
    
    # check that each has 3 food items
    for foods in result.values():
        assert isinstance(foods, list)
        assert len(foods) == 3
