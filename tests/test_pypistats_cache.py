#!/usr/bin/env python3
# encoding: utf-8
"""
Unit tests for pypistats cache
"""
import tempfile
import unittest
from pathlib import Path

from freezegun import freeze_time

import pypistats


class TestPypiStatsCache(unittest.TestCase):
    def setUp(self):
        # Choose a new cache dir that doesn't exist
        self.original_cache_dir = pypistats.CACHE_DIR
        self.temp_dir = tempfile.TemporaryDirectory()
        pypistats.CACHE_DIR = Path(self.temp_dir.name) / "pypistats"

    def tearDown(self):
        # Reset original
        pypistats.CACHE_DIR = self.original_cache_dir

    @freeze_time("2018-12-26")
    def test__cache_filename(self):
        # Arrange
        url = "https://pypistats.org/api/packages/pip/recent"

        # Act
        out = pypistats._cache_filename(url)

        # Assert
        self.assertTrue(
            str(out).endswith(
                "2018-12-26-https-pypistats-org-api-packages-pip-recent.json"
            )
        )

    def test__load_cache_not_exist(self):
        # Arrange
        filename = Path("file-does-not-exist")

        # Act
        data = pypistats._load_cache(filename)

        # Assert
        self.assertEqual(data, {})

    def test__load_cache_bad_data(self):
        # Arrange
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"Invalid JSON!")

            # Act
            data = pypistats._load_cache(Path(f.name))

        # Assert
        self.assertEqual(data, {})

    def test_cache_round_trip(self):
        # Arrange
        filename = pypistats.CACHE_DIR / "test_cache_round_trip.json"
        data = "test data"

        # Act
        pypistats._save_cache(filename, data)
        new_data = pypistats._load_cache(filename)

        # Tidy up
        filename.unlink()

        # Assert
        self.assertEqual(new_data, data)
