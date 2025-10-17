import pyshorteners
# for pyshorteners do (pip install pyshorteners)


def shorten_url(url):
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(url)
    return short_url

if __name__ == "__main__":
    url = input("Enter the URL to shorten: ")
    print("Shortened URL:", shorten_url(url))
