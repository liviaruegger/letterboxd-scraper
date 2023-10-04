import requests
import csv


def request_with_retry(
    url: str, max_retries: int = 5, timeout: float = 1.0
) -> requests.Response:
    for retry in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code == 200:
                return response

        except Exception as e:
            print(f"Request failed: {e}")

    raise Exception("Failed to perform the request")


def save_to_csv(data: dict, filename: str) -> None:
    with open(filename, "w", newline="") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)
