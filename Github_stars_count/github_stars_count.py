import requests
import sys
import time
#Show top 3 most starred repositories
#Display total forks count as bonus
#Simple CLI output


def add_if_top(top,url,qtd,podium=3):
    top.append({'qtd': qtd, 'url': url })
    return sorted(top, key=lambda repo: repo.get('qtd'), reverse=True) [0:podium]


def stars_count_github(user):
    """
    Count total stars from github user in all public repositories.
    """
    total_stars = 0
    total_forks = 0
    pg = 1
    top=[]
    while True:
        url = f"https://api.github.com/users/{user}/repos?per_page=100&page={pg}"
        while True:
          response = requests.get(url)
          if response.status_code != 200:
              if response.status_code== 403 and "API rate limit" in response.json().get("message",""):
                print("Wait 20 seconds .. api rate limit exceeded.")
                time.sleep(20)
                continue
              else:
                print(f"Github API error: {response.status_code}")          
          time.sleep(1)                
          break

        repos = response.json()
        if not repos:
            break  # Sem mais repositórios

        for repo in repos:
            qtd=repo.get("stargazers_count", 0)
            if qtd>0:
                top=add_if_top(top,repo.get('url'),qtd)
                
            total_stars += qtd
            total_forks = repo.get("forks",0)
        pg += 1

    return total_stars, total_forks, top


if __name__ == "__main__":
    if len(sys.argv) == 1:
      user = input("Username: ").strip()
    else:
      user =sys.argv[1]

    (stars, forks, top) = stars_count_github(user)
    print(f"The user '{user}' has {stars} stars 🌟.\nTheir projects have {forks} forks ⑂\n")
    if len(top)>0:
      print(f"Top stars repos:")
      [print(t.get("url"),"=>",t.get("qtd")) for t in top]
