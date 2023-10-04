from bs4 import BeautifulSoup

from utils import request_with_retry


def get_film(endpoint: str) -> str:
    url = f"https://letterboxd.com{endpoint}"
    print("Requesting:", url)

    response = request_with_retry(url)
    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to retrieve the film")


def parse_film_data(html_content: str) -> list[dict[str, str]]:
    film_soup = BeautifulSoup(html_content, "html.parser")
    header = film_soup.find("head")

    # Scrape additional info
    title = header.find("meta", property="og:title")["content"]
    director = header.find("meta", attrs={"name": "twitter:data1"})["content"]
    url = header.find("meta", property="og:url")["content"]

    # A film might not have a rating, if it wasn't rated by enough users
    try:
        average_rating = (
            header.find("meta", attrs={"name": "twitter:data2"})
            .get("content")
            .strip(" out of 5")
        )
    except:
        average_rating = "-1.00"

    # A film might not have a release year, if it's not released yet
    try:
        release_year = title.split(" (")[1].strip(")")
    except:
        release_year = "inf"

    film_info = {
        "title": title,
        "director": director,
        "release_year": release_year,
        "average_rating": average_rating,
        "url": url,
    }

    return film_info


if __name__ == "__main__":
    print(parse_film_data(get_film("/film/portrait-of-a-lady-on-fire/")))
