import unittest
from bibtexparser import Reference

class TestReferenceClass(unittest.TestCase):

    def test_wrong_input_no_at(self):
        string = "jg"
        ref = Reference(string)
        self.assertEqual(ref.type, None)
        self.assertEqual(ref.id, None)
        self.assertEqual(ref.entries, {})

    def test_wrong_input_no_first_curly(self):
        string = "@retrert grt r"
        ref = Reference(string)
        self.assertEqual(ref.type, None)
        self.assertEqual(ref.id, None)
        self.assertEqual(ref.entries, {})

    def test_empty(self):
        string = """

        @{,
        }

        """
        ref = Reference(string)
        self.assertEqual(ref.type, '')
        self.assertEqual(ref.id, '')
        self.assertEqual(ref.entries, {})

    def test_only_type(self):
        string = """
        @book {  newton1664gravity ,
        }
        """
        ref = Reference(string)
        self.assertEqual(ref.type, 'book')
        self.assertEqual(ref.id, 'newton1664gravity')
        self.assertEqual(ref.entries, {})

    def test_single_entry_white_spaces(self):
        string = """
        @book{  newton1664gravity  ,
            author  =
            "Newton, Isaac"
        }
        """
        ref = Reference(string)
        self.assertEqual(ref.type, 'book')
        self.assertEqual(ref.id, 'newton1664gravity')
        self.assertEqual(ref.entries, {"author": "Newton, Isaac"})

    def test_single_entry_no_white_spaces(self):
        string = '@book{newton1664gravity,author="Newton, Isaac"}'
        ref = Reference(string)
        self.assertEqual(ref.type, 'book')
        self.assertEqual(ref.id, 'newton1664gravity')
        self.assertEqual(ref.entries, {"author": "Newton, Isaac"})

    def test_multi_entry_white_spaces(self):
        string = """
        @book{  newton1664gravity  ,
            author  =
            "Newton, Isaac"

              ,
             year= "1664"
        }
        """
        ref = Reference(string)
        self.assertEqual(ref.type, 'book')
        self.assertEqual(ref.id, 'newton1664gravity')
        self.assertEqual(ref.entries, {"author": "Newton, Isaac", "year": "1664"})

    def test_multi_entry_no_white_spaces(self):
        string = '@book{newton1664gravity,author="Newton, Isaac",year="1664"}'
        ref = Reference(string)
        self.assertEqual(ref.type, 'book')
        self.assertEqual(ref.id, 'newton1664gravity')
        self.assertEqual(ref.entries, {"author": "Newton, Isaac", "year": "1664"})



if __name__ == '__main__':
    unittest.main()
