import requests

API_key = "0956340c49bc4d05a1d8208e2002405b"

def recipe_suggestion(ingredients, dietary_restriction):
    '''This function returns the recipe using the spoonacular API,
       based on the ingredients and dietary restriction entered by the user'''
    
    ingredients_str = ",".join(ingredients)
    url = "https://api.spoonacular.com/recipes/complexSearch"
    
    parameters = {"apiKey": API_key,
        "includeIngredients": ingredients_str,
        "diet": dietary_restriction.lower(),
        "number": 3,} #get top 3 recipes
    
    response = requests.get(url, params=parameters) #fetching the recipes from spoonacular

    #if could not fetch the recipes
    if response.status_code != 200:
        print(f"Error: Failed to fetch recipes ({response.status_code})")
        return

    
    data = response.json()
    results = data.get("results", [])
    
    #if there is a recipe for the given ingredients and dietary preference
    if results:
        for recipe in results:
            title = recipe["title"]
            recipe_id = recipe["id"]
            print(f" {title} (https://spoonacular.com/recipes/{title.replace(' ', '-')}-{recipe_id})")
    
    else: #if no recipe is found
        print("No recipe found")



def main():
    '''This is the main function that takes in the input from the user,
       fetch the desired recipe based on the input preferences and 
       prints the top 3 recipes found!!'''
    
    continue_suggesting_recipe = True
    
    #continue to take the inputs and show the recipes until the user wishes
    while (continue_suggesting_recipe):
        number_of_ingredients = int(input("Enter the number of ingredients you want to add: "))

        ingredients = [] #array to store all the ingredients
        for i in range(number_of_ingredients):
            name_of_ingredient = input("Enter the name of the ingredient available: ").strip()
            ingredients.append(name_of_ingredient)

        choice_of_restriction = input("Do you have any dietary restriction (y/n) ?: ").strip()

        if choice_of_restriction.lower() == 'y':
            print("What is your dietary restriction?")
            options = ["Vegetarian", "Vegan", "Halal", "Gluten free", "Other"]
            for i in range(len(options)):
                print(i+1,options[i])
            choice_input = input("Please enter the correct number corresponding to your dietary restriction: ").strip()

            try:
                choice = int(choice_input)
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
            else:
                if choice == 5:
                    other = input("What is your dietary preference?: ").strip()
                    print(f'Perfect! We will consider {other} as your preference!!')
                    print("Suitable recipe according to your ingredients and dietary preference is:")
                elif choice in (1,2,3,4):
                    print("Suitable recipe according to your ingredients and dietary preference is:")
                    dietary_restriction = options[choice-1]
                    if dietary_restriction.lower() == "halal":
                        dietary_restriction = ""  # Spoonacular doesn't support 'halal'
                        print("Note: Halal filtering isn't supported by Spoonacular API. Showing general recipes instead.")
                else:
                    print("Invalid input. Please choose from 1–5.")
                    continue
                
            
            recipe_suggestion(ingredients, dietary_restriction)

        else:
            print("No dietary restriction selected — showing general recipes instead.")
            recipe_suggestion(ingredients, "none")
        
        continue_choice = input("Do you want to continue for other recipes? (y/n): " )
        if continue_choice.lower() == 'n':
            continue_suggesting_recipe = False

if __name__== '__main__' :
    main()