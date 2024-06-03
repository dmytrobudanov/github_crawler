import unittest
from unittest.mock import patch, Mock
from github_crawler import get_repository_details, github_search

class TestGitHubCrawlerWithProxies(unittest.TestCase):

    @patch('requests.get')
    def test_get_repository_details(self, mock_get):
        print("Testing get_repository_details function...")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <span class="author"><a href="#">jpadilla</a></span>
        <li class="d-inline">
            <span class="color-fg-default text-bold mr-1">Python</span>
            <span>100.0%</span>
        </li>
        </html>
        """
        mock_get.return_value = mock_response

        proxies = ["194.126.37.94:8080", "13.78.125.167:8080"]
        result = get_repository_details('https://github.com/jpadilla/django-rest-framework-jwt', proxies)
        expected = {
            "owner": "jpadilla",
            "language_stats": {
                "Python": 100.0
            }
        }
        self.assertEqual(result, expected)
        print("test_get_repository_details passed.")

    @patch('requests.get')
    def test_github_search(self, mock_get):
        print("Testing github_search function...")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        {
            "hl_name":"jpadilla/django-rest-framework-jwt",
            "hl_name":"another_user/another_repo"
        }
        """

        mock_get.return_value = mock_response

        # Mock the get_repository_details to avoid real HTTP requests
        with patch('github_crawler.get_repository_details') as mock_details:
            mock_details.side_effect = [
                {"owner": "jpadilla", "language_stats": {"Python": 100.0}},
                {"owner": "another_user", "language_stats": {"Python": 80.0, "JavaScript": 20.0}}
            ]
            proxies = ["194.126.37.94:8080", "13.78.125.167:8080"]
            result = github_search(["python", "django-rest-framework", "jwt"], "Repositories", proxies)
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)  # test if there are results
            self.assertIn("url", result[0])
            self.assertIn("extra", result[0])
            self.assertIn("owner", result[0]["extra"])
            self.assertIn("language_stats", result[0]["extra"])
            print("test_github_search passed.")

if __name__ == '__main__':
    unittest.main()
