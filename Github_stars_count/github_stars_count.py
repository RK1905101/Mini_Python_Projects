import requests
import sys

def stars_count_github(user):
    """
    Count total stars from github user in all public repositories.
    """
    total_stars = 0
    pg = 1

    while True:
        url = f"https://api.github.com/users/{user}/repos?per_page=100&page={pg}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Github API error: {response.status_code}")
            break

        repos = response.json()
        if not repos:
            break  # Sem mais repositórios

        for repo in repos:
            total_stars += repo.get("stargazers_count", 0)

        pg += 1

    return total_stars


if __name__ == "__main__":
    if len(sys.argv) == 1:
      user = input("Username: ").strip()
    else:
      user =sys.argv[1]

    estrelas = stars_count_github(user)
    print(f"The user '{user}' has {estrelas} stars 🌟")