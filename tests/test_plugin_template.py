import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_template import Template

def test_check_bits():
	print('Running test template')

	template = Template()

	assert template.checkBits(0) == False
	assert template.checkCat('admin') == True
	assert template.checkCat('arrow') == False
