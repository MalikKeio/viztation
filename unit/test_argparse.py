import unittest
from viztation import parser
from latexparser import LaTexFile
from bibtexparser import BibTexFile

class TestReferenceClass(unittest.TestCase):

    def test_nothing(self):
        args = parser.parse_args([])
        self.assertEqual(args.tex, [])
        self.assertEqual(args.bib, [])

    def test_two_tex_files(self):
        args = parser.parse_args('--tex unit/cite.tex unit/latex1.tex'.split())
        latex0 = LaTexFile(args.tex[0])
        latex1 = LaTexFile(args.tex[1])
        self.assertCountEqual(latex0.cites, ['baker2011foundations', 'independent2015bac',
                         'w3techs2014usage', 'feng2007bilingual',
                         'w3techs2014usage', 'feng2007bilingual','epi2014epi',
                         'laka2014mandela', 'toeic2015toeic'])
        self.assertCountEqual(latex1.cites, ['laka2014mandela', 'baker2011foundations',
                                             'freire2008provenance', 'steele2010beautiful',
                                             'silva2011using', 'ruan2011cloud'])
        self.assertEqual(args.bib, [])

    def test_two_bib_files(self):
        args = parser.parse_args('--bib unit/cf.bib unit/lot.bib'.split())
        bibtex0 = BibTexFile(args.bib[0])
        bibtex1 = BibTexFile(args.bib[1])
        self.assertEqual(len(bibtex0.references), 30)
        self.assertEqual(len(bibtex1.references), 35)
        self.assertEqual(args.tex, [])
