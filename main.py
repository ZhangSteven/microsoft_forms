# coding=utf-8
#
# Read BOCHK holding and cash reports, convert them to Geneva holding and cash
# format.
# 
# Program structure very similar to nomura.main.py
# 

from functools import partial
from itertools import chain
from utils.utility import dictToValues, writeCsv
from toolz.functoolz import compose
from nomura.main import fileToLines, getHeadersnLines
from os.path import join, dirname, abspath
import logging
logger = logging.getLogger(__name__)




"""
	[String] file => [Iterable] positions

	position: [Dictionary] header -> value
"""
getRawHoldingPositions = compose(
	  lambda t: map(lambda line: dict(zip(t[0], line)), t[1])
	, getHeadersnLines
	, fileToLines
)



"""
	[Iterable] records => [Iterable] records

	Using email address as the key, filter out only the lastest record
	by that email address.
"""
consolidate = compose(
	  lambda d: d.values()
	, dict
	, partial(map, lambda r: (r['Email'], r))
)



"""
	Get the absolute path to the directory where this module is in.

	This piece of code comes from:

	http://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python
"""
getCurrentDirectory = lambda: \
	dirname(abspath(__file__))



"""
	Change this function to the list of headers you want to output.

	Usually it is the list of headers in the input file.
"""
getHeaders = lambda: \
	['ID', 'Start time', 'Completion time', 'Email', 'Name', 'Item']



"""
	[String] inputFile => [String] output csv file name

	Side effect: Write the output csv file, named "poll_result.csv" in the 
	local directory.
"""
outputCsv = compose(
	  partial(writeCsv, 'poll_result.csv')
	, lambda records: \
		chain( [getHeaders()]
			 , map( partial(dictToValues, getHeaders())
			 	  , records))
	, consolidate
	, getRawHoldingPositions
)




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	"""
		Copy the Microsoft forms poll result, exported as an Excel file, 
		to the local directory, then

		$ python main.py <file name>

		The output csv files are written in the local directory as well.

		Note two things:

		1. If the input file has Chinese characters as column headers, change
			them into English.
		2. Modify the getHeaders() function to suite your needs.
	"""
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', metavar='"export file from microsoft forms"')
	args = parser.parse_args()

	outputCsv(args.file)