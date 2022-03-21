import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_template import Template
from injectables.discord_dependencies import *

class TestTemplate(unittest.TestCase):

	def test_check_bits(self):
		template = Template()
		assert template.checkBits(0) == False

	def test_check_cat_true(self):
		template = Template()
		assert template.checkCat('admin') == True

	def test_check_cat_false(self):
		template = Template()
		assert template.checkCat('arrow') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	async def test_run_cheer(self):
		template = Template()
		assert await template.runCheer('potato', 0) == True

	async def test_run(self):
		template = Template()
		assert await template.run('potato', 0) == True

	async def test_stop(self):
		template = Template()
		await template.stop('potato')

if __name__ == '__main__':
	unittest.main()