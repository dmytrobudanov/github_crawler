import requests
import re
import json
from bs4 import BeautifulSoup
import random

def get_repository_details(repo_url, proxies):
    try:
        proxy = {"http": random.choice(proxies)}
        response = requests.get(repo_url, proxies=proxy)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during request to {repo_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    owner = soup.select_one('span.author a').text.strip()

    language_stats = {}
    language_elements = soup.select('li.d-inline')

    print(f"Analyzing repository: {repo_url}")
    print("Language elements found:", len(language_elements))

    for element in language_elements:
        lang_name_element = element.select_one('span.color-fg-default.text-bold.mr-1')
        lang_percent_element = element.select_one('span:not(.color-fg-default.text-bold.mr-1)')

        if lang_name_element and lang_percent_element:
            lang_name = lang_name_element.text.strip()
            lang_percent = lang_percent_element.text.strip().strip('%').replace(' ', '')

            if lang_name.lower() == 'other':
                continue

            try:
                language_stats[lang_name] = float(lang_percent)
            except ValueError:
                print(f"Could not convert '{lang_percent}' to float for '{lang_name}' in repository: {repo_url}")

    return {"owner": owner, "language_stats": language_stats}

def github_search(keywords, search_type, proxies):
    search_url = f"https://github.com/search?q={'%20'.join(keywords)}&type={search_type}"

    try:
        proxy = {"http": random.choice(proxies)}
        response = requests.get(search_url, proxies=proxy)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return []

    with open('github_search.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    # Regular expressions to find all occurrences of hl_name with hrefs
    matches = re.findall(r'"hl_name":"(.*?)"', response.text)

    if not matches:
        print("No links found on the page.")
        return []

    results = []
    for match in matches:
        repo_url = f"https://github.com/{match.replace('<em>', '').replace('</em>', '')}"
        details = get_repository_details(repo_url, proxies)
        if details:
            results.append({"url": repo_url, "extra": details})

    print(f"Found {len(results)} links with details.")
    return results

if __name__ == "__main__":
    input_data = {
        "keywords": ["python", "django-rest-framework", "jwt"],
        "proxies": ["194.126.37.94:8080", "13.78.125.167:8080"],
        "type": "Repositories"
    }

    results = github_search(input_data["keywords"], input_data["type"], input_data["proxies"])
    print(json.dumps(results, indent=2))
