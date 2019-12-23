# coding=utf-8
# 

import unittest2
from os.path import join
from toolz.functoolz import compose
from utils.iter import firstOf
from microsoft_forms.main import getRawHoldingPositions, consolidate, getCurrentDirectory



class TestALL(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestALL, self).__init__(*args, **kwargs)



	def testConsolidate(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'poll_result.xlsx')
		records = compose(
			  list
			, consolidate
			, getRawHoldingPositions
		)(inputFile)

		self.assertEqual(44, len(records))
		self.assertEqual(1, len(list(filter( lambda p: p['Email'] == 'anizer.lam@CLAMC.COM.HK'
										   , records))))
		self.assertEqual(1, len(list(filter( lambda p: p['Email'] == 'eddie.chia@CLAMC.COM.HK'
										   , records))))
		self.assertEqual( 'Surface laptop (Intel i5/8GB RAM/128GB SSD)'
						, firstOf( lambda p: p['Email'] == 'anizer.lam@CLAMC.COM.HK'
								 , records)['Item'])
