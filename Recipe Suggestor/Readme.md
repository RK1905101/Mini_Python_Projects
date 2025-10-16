# Recipe Suggestor

## Description
is a Python-based project that suggests recipes based on the ingredients you already have at home. It also considers dietary preferences or restrictions — such as vegetarian, vegan, or gluten-free — and fetches real recipes using the Spoonacular API which indeed help users quickly find suitable meal ideas without needing to search endlessly online.

## Features
- Input a list of ingredients you currently have and get top 3 recipes instantly.
- Filter recipes by dietary preferences (e.g., vegetarian, vegan, gluten-free, etc.).
- Interactive loop – after getting results, you can choose to continue searching for more recipes.
- Real-time recipe data – fetched directly from the Spoonacular public API.
- Automatic recipe links – each recipe result includes a clickable link to view the full recipe online.

## Requirements
- Python 3.x
- Internet connection (to fetch recipes from the Spoonacular API)
- A Spoonacular API key (free registration)

## Installation
- pip install requests
- API_key = "your_api_key_here" (Open the file Recipe_suggestor.py and replace the placeholder with your own API key)


## Usage
'''bash
python3 Recipe_suggestor.py
'''

## Important Note
- If you choose “Halal”, the API will show general recipes (as Spoonacular doesn’t support that filter).
- You may need to sign up on spoonacular.com/food-api to obtain a free API key.
- API requests are limited on the free plan (150/day).