import unittest
import subprocess


class TestDirwatcher(unittest.TestCase):
    """Tests functionality of dirwatcher.py"""

    def test_searchstring(self):
        """Tests if the search string is found in the given directory"""
        process = subprocess.Popen(
            ["python", "./dirwatcher.py", "1", "Hello", "-d .", "-t txt"],
            stdout=subprocess.PIPE)
        stdout, _ = process.communicate().decode("utf-8")
        self.assertTrue(stdout)


if __name__ == '__main__':
    unittest.main()
