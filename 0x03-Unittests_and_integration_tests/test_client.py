#!/usr/bin/env python3
"""Unittests and integration tests for client.py"""

import unittest
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected value."""
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"name": org_name})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL from org property."""
        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://fakeurl.com"}
            self.assertEqual(client._public_repos_url, "http://fakeurl.com")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct repo list."""
        payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}}
        ]
        mock_get_json.return_value = payload
        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fakeurl.com"
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("http://fakeurl.com")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean value."""
        client = GithubOrgClient("org")
        self.assertEqual(client.has_license(repo, license_key), expected)

# Integration tests
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(org_payload, repos_payload, expected_repos, apache2_repos)]
)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up class with patched requests.get."""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url.endswith("/repos"):
                return type("Response", (), {"json": lambda: cls.repos_payload})()
            return type("Response", (), {"json": lambda: cls.org_payload})()
        
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list."""
        client = GithubOrgClient("org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license."""
        client = GithubOrgClient("org")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
