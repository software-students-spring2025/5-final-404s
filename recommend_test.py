'''pytest tests for recommend.py'''


from recommend import main
#import pytest


def test_food_recommendations_for_carbs(capsys, monkeypatch):
    '''test for carbs'''

    monkeypatch.setattr('builtins.input', lambda: 'carbs')
    main()

    captured = capsys.readouterr()
    output = captured.out.strip()
    expected_output = {'bread', 'pasta', 'rice',
                            'potatoes', 'corn',
                            'chips', 'oats', 'nuts',
                            'fruit'}

    # pylint: disable=eval-used
    output_set = eval(output)

    assert output_set == expected_output





def test_food_recommendations_for_fruit(capsys, monkeypatch):
    '''test for fruit'''

    monkeypatch.setattr('builtins.input', lambda: 'fruit')
    main()

    captured = capsys.readouterr()
    output = captured.out.strip()
    expected_output = {'bananas', 'blueberries', 'oranges',
                            'strawberries', 'kiwis',
                            'mangos', 'blackberries',
                            'raspberries', 'apples', 'peaches', 
                            'plums'}

    # pylint: disable=eval-used
    output_set = eval(output)

    assert output_set == expected_output





def test_food_recommendations_for_vegetables(capsys, monkeypatch):
    '''test for vegetables'''

    monkeypatch.setattr('builtins.input', lambda: 'vegetables')
    main()

    captured = capsys.readouterr()
    output = captured.out.strip()
    expected_output = {'broccoli', 'onions', 'beets',
                            'carrots','radishes', 'turnips',
                            'parsnips', 'asparagus',
                            'celery', 'lettuce', 'spinach',
                            'kale', 'arugula',
                            'cauliflower', 'artichoke'}

    # pylint: disable=eval-used
    output_set = eval(output)

    assert output_set == expected_output





def test_food_recommendations_for_protein(capsys, monkeypatch):
    '''test for protein'''

    monkeypatch.setattr('builtins.input', lambda: 'protein')
    main()

    captured = capsys.readouterr()
    output = captured.out.strip()
    expected_output = {'fish', 'chicken', 'eggs', 'nuts',
                            'seeds', 'lentils',
                            'yogurt', 'milk',
                            'beans', 'tofu', 'quinoa',
                            'turkey','salmon', 'edamame',
                            'chickpeas', 'pork', 'cheese',
                            'tempeh'}

    # pylint: disable=eval-used
    output_set = eval(output)

    assert output_set == expected_output





def test_food_recommendations_invalid_input(capsys, monkeypatch):
    '''test for invalid input'''

    monkeypatch.setattr('builtins.input', lambda: 'invalid')
    main()

    captured = capsys.readouterr()
    output = captured.out.strip()

    assert output == ""
