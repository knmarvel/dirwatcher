import unittest
import subprocess
import dirwatcher


class TestDirwatcher(unittest.TestCase):
    """Tests functionality of dirwatcher.py"""

    def test_searchstring(self):
        answer = [['/Users/nynaeve/Kenzie/todo-dirwatcher', 9]]
        fromblah = dirwatcher.check_for_string("Hello", ".", "txt")
        self.assertEqual(fromblah, answer)


if __name__ == '__main__':
    unittest.main()
