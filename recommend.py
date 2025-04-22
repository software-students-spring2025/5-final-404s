'''
python program to recommend food 
based on deficit


when we set up the rest of the program, we will 
create a variable that can be inserted into the 
functions below

'''



variable = input()



def main():
    '''main function'''


    #food groups for defecits
    #categories = {'carbs', 'protein', 'fruit', 'vegetables'}


    #just simple if statement for now
    #at least until we figure out how we
    #are taking the input

    if variable == 'carbs':
        recommend_options = {'bread', 'pasta', 'rice',
                            'potatoes', 'corn',
                            'chips', 'oats', 'nuts',
                            'fruit'}

        print(recommend_options)



    if variable == 'fruit':
        recommend_options = {'bananas', 'blueberries', 'oranges',
                            'strawberries', 'kiwis',
                            'mangos', 'blackberries',
                            'raspberries', 'apples', 'peaches', 
                            'plums'}

        print(recommend_options)



    if variable == 'vegetables':
        recommend_options = {'broccoli', 'onions', 'beets',
                            'carrots','radishes', 'turnips',
                            'parsnips', 'asparagus',
                            'celery', 'lettuce', 'spinach',
                            'kale', 'arugula',
                            'cauliflower', 'artichoke'}

        print(recommend_options)



    if variable == 'protein':
        recommend_options = {'fish', 'chicken', 'eggs', 'nuts',
                            'seeds', 'lentils',
                            'yogurt', 'milk',
                            'beans', 'tofu', 'quinoa',
                            'turkey','salmon', 'edamame',
                            'chickpeas', 'pork', 'cheese',
                            'tempeh'}

        print(recommend_options)
