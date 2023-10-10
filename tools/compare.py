from watchlist import get_complete_watchlist_data
from film import get_film, parse_film_data
from utils import save_to_csv


def compare_watchlists(users: list[str]) -> list:
    watchlists = []

    for user in users:
        watchlists.append(
            [
                f["endpoint"]
                for f in get_complete_watchlist_data(
                    username=user, complete_data=False
                )
            ]
        )

    films_in_common = set(watchlists[0])
    for watchlist in watchlists[1:]:
        films_in_common = films_in_common.intersection(set(watchlist))
    print(f"\n --- found {len(films_in_common)} films in common ---")

    film_data = []

    print(f"\n === Collecting film details ===")
    for endpoint in films_in_common:
        film_data.append(parse_film_data(get_film(endpoint)))

    return film_data


def save_comparison_to_csv(
    users: list[str], sort_by_rating: bool = False
) -> None:
    data = compare_watchlists(users)

    if sort_by_rating:
        data = sorted(data, key=lambda x: x["average_rating"], reverse=True)

    save_to_csv(data, f"{users[0]}_and_friends.csv")


if __name__ == "__main__":
    users = []

    _input = input("Enter username: ")
    while _input != "q":
        users.append(_input)
        _input = input("Enter username (or 'q' when you're done): ")

    save_comparison_to_csv(users, True)
