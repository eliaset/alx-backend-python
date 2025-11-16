#!/usr/bin/env python3
"""Tests for client module (Tasks 4 & 5)."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    # ---------- Task 4: Parameterize and patch as decorators ----------
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
    # ------------------------------------------------------------------

    # ---------- Task 5: Mocking a property ----------
    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL."""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = org_payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, org_payload["repos_url"])
    # ------------------------------------------------------------------
