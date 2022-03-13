import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_template import Template

def test_check_bits():
	template = Template()
	assert template.checkBits(0) == False

def test_check_cat_true():
	template = Template()
	assert template.checkCat('admin') == True

def test_check_cat_false():
	template = Template()
	assert template.checkCat('arrow') == False

def test_raise_exception_check_cat():
	template = Template()
	with pytest.raises(TypeError):
		template.checkCat(0)