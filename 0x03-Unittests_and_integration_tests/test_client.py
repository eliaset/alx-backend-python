#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    # ------------------------
    # Task 4: Parameterize and patch as decorators
    # ------------------------
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value."""
        expected = {"org": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    # ------------------------
    # Task 5: Mocking a property
    # ------------------------
    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL."""
        payload = {"repos_url": "http://example.com/repos"}
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    # ------------------------
    # Task 6: More patching
    # ------------------------
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns list of repo names."""
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = repos_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://example.com/repos"
            client = GithubOrgClient("google")
            self.assertEqual(
                client.public_repos(),
                ["repo1", "repo2", "repo3"]
            )
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "http://example.com/repos"
            )

    # ------------------------
    # Task 7: Parameterize
    # ------------------------
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get for org and repos."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Side effect for requests.get(url).json()
        def json_side_effect(*args, **kwargs):
            url = args[0]
            if url.endswith("/repos"):
                return cls.repos_payload
            return cls.org_payload

        mock_get.return_value = Mock(json=json_side_effect)

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns expected list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: public_repos filtered by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )
