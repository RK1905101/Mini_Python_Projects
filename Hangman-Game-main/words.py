import random

# Word categories with different difficulty levels
word_categories = {
    "Animals": {
        "easy": ["elephant", "giraffe", "kangaroo", "penguin", "dolphin", "butterfly", "cheetah", "crocodile"],
        "medium": ["jaguar", "falcon", "turtle", "rabbit", "monkey", "tiger"],
        "hard": ["zebra", "panda", "koala", "hyena", "otter"]
    },
    "Movies": {
        "easy": ["titanic", "avatar", "frozen", "inception", "gladiator", "jaws"],
        "medium": ["matrix", "joker", "rocky", "alien", "rocky"],
        "hard": ["memento", "psycho", "fargo", "ghost"]
    },
    "Countries": {
        "easy": ["australia", "germany", "canada", "brazil", "mexico", "portugal", "argentina"],
        "medium": ["france", "japan", "india", "egypt", "spain"],
        "hard": ["nepal", "malta", "qatar", "chile"]
    },
    "Food": {
        "easy": ["hamburger", "spaghetti", "sandwich", "pancakes", "chocolate", "blueberry"],
        "medium": ["pizza", "taco", "sushi", "curry", "waffle"],
        "hard": ["bagel", "mango", "pasta", "bacon"]
    },
    "Sports": {
        "easy": ["football", "baseball", "basketball", "swimming", "volleyball", "cricket"],
        "medium": ["soccer", "hockey", "tennis", "rugby"],
        "hard": ["judo", "polo", "golf", "surf"]
    },
    "Technology": {
        "easy": ["computer", "keyboard", "internet", "software", "database", "algorithm"],
        "medium": ["python", "server", "coding", "laptop"],
        "hard": ["debug", "cache", "byte", "loop"]
    },
    "Music": {
        "easy": ["symphony", "harmony", "rhythm", "melody", "acoustic", "orchestra"],
        "medium": ["guitar", "piano", "drums", "vocal", "jazz"],
        "hard": ["tempo", "chord", "bass", "note"]
    },
    "Science": {
        "easy": ["chemistry", "biology", "gravity", "molecule", "planet", "hydrogen"],
        "medium": ["oxygen", "carbon", "energy", "atoms"],
        "hard": ["quark", "plasma", "proton", "light"]
    },
    "Nature": {
        "easy": ["mountain", "waterfall", "rainbow", "sunrise", "forest", "desert"],
        "medium": ["ocean", "river", "storm", "beach", "cloud"],
        "hard": ["delta", "cliff", "canyon", "lunar"]
    },
    "Colors": {
        "easy": ["crimson", "turquoise", "lavender", "emerald", "scarlet", "violet"],
        "medium": ["orange", "purple", "yellow", "silver"],
        "hard": ["amber", "coral", "maroon", "ivory"]
    }
}

def get_random_word(category, difficulty):
    """
    Get a random word based on category and difficulty
    
    Args:
        category: String - the category name
        difficulty: String - '1' (easy), '2' (medium), '3' (hard)
    
    Returns:
        String - a random word from the selected category and difficulty
    """
    difficulty_map = {
        '1': 'easy',
        '2': 'medium',
        '3': 'hard'
    }
    
    diff_level = difficulty_map.get(difficulty, 'medium')
    
    if category in word_categories:
        word_list = word_categories[category][diff_level]
        return random.choice(word_list)
    else:
        # Fallback to random category
        random_category = random.choice(list(word_categories.keys()))
        word_list = word_categories[random_category][diff_level]
        return random.choice(word_list)

def get_all_words():
    """Get all words from all categories (for testing)"""
    all_words = []
    for category in word_categories.values():
        for difficulty in category.values():
            all_words.extend(difficulty)
    return all_words
