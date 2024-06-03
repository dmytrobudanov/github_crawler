# github_crawler
Test Task

This code meets all the criteria specified in the assignment, namely:
Python 3
- The crawler should be as efficient as possible (fast, low memory consumption, low CPU load, ...) Input data:
- Search keywords: a list of keywords to be used as search queries (unicode characters must be supported)
- List of proxy servers: one of them should be selected and used randomly to execute all HTTP requests (you can get a free list of proxy servers to work with at https://free-proxy-list.net/)
- Type: the type of object we are looking for (repositories, releases, and wikis should be supported)
- Documentation on how to use it should be included
- Output: URLs for each of the search results
- The code should also contain unit tests with a minimum code coverage of 90%.
- For the purposes of this assignment, you only need to process the first page results
- For this assignment, we want to work with raw HTML, the JSON API cannot be used.
- You can use any libraries you find useful for the task (e.g. HTTP libraries, parsers,...), but not frameworks (e.g. Scrapy)

Optional:
- Repository owner
- Language statistics.

It is designed to search GitHub repositories using specified keywords and extract detailed information about each repository found.

Translated with DeepL.com (free version)

Requirements:
Python 3
requests
beautifulsoup
re

Prepare Input Data:
Create a JSON object with the following structure to define your search criteria:
{
  "keywords": ["python", "django-rest-framework", "jwt"],
  "proxies": ["194.126.37.94:8080", "13.78.125.167:8080"],
  "type": "Repositories"
}

Run the Script and Unit Tests
