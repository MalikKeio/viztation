import unittest
from bibtexparser import Reference
from bibtexparser import BibTexFile
from latexparser import LaTexFile

class TestReferenceClass(unittest.TestCase):

    def test_empty_input(self):
        string = ""
        ref = Reference(string)
        self.assertEqual(ref.type, None)
        self.assertEqual(ref.id, None)
        self.assertEqual(ref.entries, {})

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

    def test_real_life_reference(self):
        string = """
        @misc{independent2015bac,
  author="Sehmer, Alexander",
  title="French students concerned they're not `coping' with English exam question",
  howpublished="\href{http://www.independent.co.uk/news/world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}{http://www.independent.co.uk/news/ world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}",
  year="June 22, 2015",
  note="[Online; Retrieved on July 4, 2015]"
}"""
        ref = Reference(string)
        self.assertEqual(ref.type, 'misc')
        self.assertEqual(ref.id, 'independent2015bac')
        self.assertEqual(ref.entries["author"], "Sehmer, Alexander")
        self.assertEqual(ref.entries["title"], "French students concerned they're not `coping' with English exam question")
        self.assertEqual(ref.entries["howpublished"], "\href{http://www.independent.co.uk/news/world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}{http://www.independent.co.uk/news/ world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}")
        self.assertEqual(ref.entries["year"], "June 22, 2015")
        self.assertEqual(ref.entries["note"], "[Online; Retrieved on July 4, 2015]")

    def test_real_life_curly_reference(self):
        string = """
        @misc{independent2015bac,
  author={Sehmer, Alexander},
  title={French students concerned they're not `coping' with English exam question},
  howpublished={\href{http://www.independent.co.uk/news/world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}{http://www.independent.co.uk/news/ world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}},
  year={June 22, 2015},
  note={[Online; Retrieved on July 4, 2015]}
}"""
        ref = Reference(string)
        self.assertEqual(ref.type, 'misc')
        self.assertEqual(ref.id, 'independent2015bac')
        self.assertEqual(ref.entries["author"], "Sehmer, Alexander")
        self.assertEqual(ref.entries["title"], "French students concerned they're not `coping' with English exam question")
        self.assertEqual(ref.entries["howpublished"], "\href{http://www.independent.co.uk/news/world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}{http://www.independent.co.uk/news/ world/europe/french-students-call-on-education-minister-to-cancel-tricky-english-exam-question-10336986.html}")
        self.assertEqual(ref.entries["year"], "June 22, 2015")
        self.assertEqual(ref.entries["note"], "[Online; Retrieved on July 4, 2015]")


class TestBibTexFileClass(unittest.TestCase):

    def test_empty_file(self):
        filename = 'unit/empty.bib'
        bibtexfile = BibTexFile(filename)
        self.assertEqual(bibtexfile.filename, 'unit/empty.bib')
        self.assertEqual(bibtexfile.references, [])

    def test_one_file(self):
        filename = 'unit/one.bib'
        bibtexfile = BibTexFile(filename)
        self.assertEqual(bibtexfile.filename, 'unit/one.bib')
        self.assertEqual(len(bibtexfile.references), 1)
        self.assertEqual(bibtexfile.references[0].type, 'book')
        self.assertEqual(bibtexfile.references[0].id, 'feng2007bilingual')
        self.assertEqual(bibtexfile.references[0].entries['title'], 'Bilingual education in {C}hina: practices, policies, and concepts')
        self.assertEqual(bibtexfile.references[0].entries['author'], 'Feng, Anwei')
        self.assertEqual(bibtexfile.references[0].entries['volume'], '64')
        self.assertEqual(bibtexfile.references[0].entries['year'], '2007')
        self.assertEqual(bibtexfile.references[0].entries['publisher'], 'Multilingual Matters')

    def test_two_file(self):
        filename = 'unit/two.bib'
        bibtexfile = BibTexFile(filename)
        self.assertEqual(bibtexfile.filename, 'unit/two.bib')
        self.assertEqual(len(bibtexfile.references), 2)
        self.assertEqual(bibtexfile.references[0].type, 'book')
        self.assertEqual(bibtexfile.references[0].id, 'feng2007bilingual')
        self.assertEqual(bibtexfile.references[0].entries['title'], 'Bilingual education in {C}hina: practices, policies, and concepts')
        self.assertEqual(bibtexfile.references[0].entries['author'], 'Feng, Anwei')
        self.assertEqual(bibtexfile.references[0].entries['volume'], '64')
        self.assertEqual(bibtexfile.references[0].entries['year'], '2007')
        self.assertEqual(bibtexfile.references[0].entries['publisher'], 'Multilingual Matters')
        self.assertEqual(bibtexfile.references[1].type, 'book')
        self.assertEqual(bibtexfile.references[1].id, 'baker2011foundations')
        self.assertEqual(bibtexfile.references[1].entries['title'], 'Foundations of bilingual education and bilingualism')
        self.assertEqual(bibtexfile.references[1].entries['author'], 'Baker, Colin')
        self.assertEqual(bibtexfile.references[1].entries['edition'], '4')
        self.assertEqual(bibtexfile.references[1].entries['year'], '2011')
        self.assertEqual(bibtexfile.references[1].entries['publisher'], 'Multilingual Matters')

    def test_lot_file(self):
        filename = 'unit/lot.bib'
        bibtexfile = BibTexFile(filename)
        self.assertEqual(bibtexfile.filename, 'unit/lot.bib')
        self.assertEqual(len(bibtexfile.references), 35)

    def test_ueda_bib_trailing_comma(self):
        bibtexfile = BibTexFile('unit/ueda.bib')
        self.assertEqual(bibtexfile.filename, 'unit/ueda.bib')
        self.assertEqual(len(bibtexfile.references), 1)
        self.assertEqual(bibtexfile.references[0].type, 'inproceedings')
        self.assertEqual(bibtexfile.references[0].id, 'ueda2015adsorptive')
        self.assertEqual(bibtexfile.references[0].entries['author'], 'Ueda, Kazuhide and Fujishiro, Issei')
        self.assertEqual(bibtexfile.references[0].entries['title'], 'Adsorptive {SPH} for Directable Bleeding Simulation')
        self.assertEqual(bibtexfile.references[0].entries['booktitle'], 'Proceedings of the 14th ACM SIGGRAPH International Conference on Virtual Reality Continuum and Its Applications in Industry')
        self.assertEqual(bibtexfile.references[0].entries['series'], "VRCAI '15")
        self.assertEqual(bibtexfile.references[0].entries['year'], '2015')
        self.assertEqual(bibtexfile.references[0].entries['isbn'], '978-1-4503-3940-7')
        self.assertEqual(bibtexfile.references[0].entries['location'], 'Kobe, Japan')
        self.assertEqual(bibtexfile.references[0].entries['pages'], '9--16')
        self.assertEqual(bibtexfile.references[0].entries['numpages'], '8')
        self.assertEqual(bibtexfile.references[0].entries['url'], 'http://doi.acm.org/10.1145/2817675.2817684')
        self.assertEqual(bibtexfile.references[0].entries['doi'], '10.1145/2817675.2817684')
        self.assertEqual(bibtexfile.references[0].entries['acmid'], '2817684')
        self.assertEqual(bibtexfile.references[0].entries['publisher'], 'ACM')
        self.assertEqual(bibtexfile.references[0].entries['address'], 'New York, NY, USA')
        self.assertEqual(bibtexfile.references[0].entries['keywords'], 'SPH, adsorption, bleeding, fluid simulation, guide')


class TestLaTexFileClass(unittest.TestCase):
    def test_single_cite_file(self):
        latex = LaTexFile('unit/cite.tex')
        # check that the two lists have the same elements in the same number, regardless of their order
        self.assertCountEqual(latex.cites, ['laka2014mandela', 'baker2011foundations', 'independent2015bac', 'w3techs2014usage', 'feng2007bilingual', 'w3techs2014usage', 'feng2007bilingual', 'epi2014epi', 'toeic2015toeic'])
