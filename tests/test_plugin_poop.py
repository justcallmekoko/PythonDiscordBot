import os
import sys
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_poop import Poop
from injectables.discord_dependencies import *

class TestPoop(unittest.TestCase):
    def test_checkCat_admin(self):
        poop = Poop()
        assert poop.checkCat('admin') == True
    
    def test_checkCat_false(self):
        poop = Poop()
        assert poop.checkCat('poop') == False
    
    def test_checkCat_empty(self):
        poop = Poop()
        assert poop.checkCat(None) == False

    def test_checkBits_true(self):
        poop = Poop()
        assert poop.checkBits('Please kill me') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
    async def test_runCheer(self):
        poop = Poop()
        assert await poop.runCheer('Your Mom', 100) == True
    
    async def test_run(self):
        poop = Poop()
        chan = channel()
        msg = message('Yo', chan)
        assert await poop.run(msg, '') == True
    
    async def test_stop(self):
        poop = Poop()
        await poop.stop('poop')

if __name__ == '__main__':
	unittest.main()