import os
import sys
import pytest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_help import Help

def test_check_bits():
	help = Help()
	assert help.checkBits(0) == False

def test_check_cat_true():
	help = Help()
	assert help.checkCat('admin') == True

def test_check_cat_false():
	help = Help()
	assert help.checkCat('arrow') == False
