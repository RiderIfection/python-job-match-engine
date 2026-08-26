import unittest
from matcher import rank
class MatcherTests(unittest.TestCase):
    def test_best_match(self):
        jobs=[{"id":"1","title":"Python","description":"python sql api"},{"id":"2","title":"Design","description":"figma css"}]
        self.assertEqual(rank("python sql docker",jobs)[0]["id"],"1")
if __name__=="__main__": unittest.main()
