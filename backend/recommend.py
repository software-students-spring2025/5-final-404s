import random

# used National Institutes of Health for recommend values
# https://ods.od.nih.gov/HealthInformation/dailyvalues.aspx
daily_recommended = {
    "calories": 2000,
    "protein": 50,
    "carbohydrates": 275,
    "fiber": 28,
    "calcium": 1300
}

food_options = {
    "calories": ["granola", "avocado", "nuts", "quinoa", "dried fruits", "peanut butter"],
    "protein": ["chicken", "beef", "eggs", "fish", "lentils", "turkey", "pork"],
    "carbohydrates": ["bread", "pasta", "rice", "oats", "potatoes", "tortillas"],
    "fiber": ["beans", "broccoli", "spinach", "lettuce", "chia seeds"],
    "calcium": ["milk", "yogurt", "cheese", "cottage cheese", "kale"]
}

def recommend_meal(nutrition):
    """
    Given nutrition data for a meal, recommend a few meals based on nutrient most needed
    """
    percentages = {}
    for nutrient, amount in nutrition.items():
        recommended = daily_recommended[nutrient]
        percentages[nutrient] = (amount / recommended) * 100
    
    # sort items and get 2 lowest
    sorted_items = sorted(percentages.items(), key=lambda i: i[1])
    first, _ = sorted_items[0]
    second, _ = sorted_items[1]

    # get 3 recommendations for each category
    recommendations = {
        first: random.sample(food_options[first], 3),
        second: random.sample(food_options[second], 3)
    }

    return recommendations