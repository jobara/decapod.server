import sys
import os
import unittest
import shutil
import glob
sys.path.append(os.path.abspath('..'))
import decapod_utilities as utils

class CommandInvokationTests(unittest.TestCase):
                        
    def test_01_invokeCommandSync_valid(self):
        # Test a basic command line program
        expectedOutput = "Hello Test!"
        cmd = ["echo", expectedOutput]
        output = utils.invokeCommandSync(cmd,
                                         Exception,
                                         "An error occurred while invoking a command line program")
        self.assertEquals(expectedOutput + "\n", output)
        
    def test_02_invokeCommandSync_invalid(self):
        # Test a program that doesn't exist.
        cmd = ["this_command_doesnt_exist", "--foo"]
        self.assertRaises(Exception, utils.invokeCommandSync, cmd, Exception, "inovkeCommand correctly throws an exception")

class DirectoryCreationTests(unittest.TestCase):
    
    newTestDir = os.path.abspath("new_dir")
    existingTestDir = os.path.abspath("existing_dir")
    
    def setUp(self):
        if not os.path.exists(self.existingTestDir):
            os.mkdir(self.existingTestDir)
    
    def tearDown(self):
        if os.path.exists(self.newTestDir):
            shutil.rmtree(self.newTestDir)
            
    def assertDirExists(self, path):           
        self.assertTrue(os.path.exists(path), "The test directory should be there.")
        self.assertTrue(os.path.isdir(path), "The path created should actually be a directory.")
            
    def test_01_mkdirIfNecessary_create(self):
        utils.mkdirIfNecessary(self.newTestDir)
        self.assertDirExists(self.newTestDir)
        
    def test_02_mkdirIfNecessary_existing(self):
        utils.mkdirIfNecessary(self.existingTestDir)
        self.assertDirExists(self.existingTestDir)
            
    def test_03_remakeDir_create(self):
        utils.remakeDir(self.newTestDir)
        self.assertDirExists(self.newTestDir)

    def test_04_remakeDir_existing(self):
        utils.remakeDir(self.existingTestDir)
        self.assertDirExists(self.existingTestDir)
        
if __name__ == '__main__':
    unittest.main()
