import unittest
from bibtexparser import Reference

class TestReferenceClass(unittest.TestCase):

  def test_empty(self):
      string = """
      @{,
      }
      """
      ref = Reference(string)
      self.assertEqual(ref.type, '')
      self.assertEqual(ref.id, '')
      self.assertEqual(ref.entries, {})

if __name__ == '__main__':
    unittest.main()
