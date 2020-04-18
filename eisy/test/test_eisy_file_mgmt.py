import os
import sys
import unittest

from eisy import eisy_file_mgmt
# from eisy.eisy_file_mgmt import *

module_path = os.path.abspath(os.path.join('../'))
if module_path not in sys.path:
    sys.path.append(module_path)

# import eisy.simulation.circuits as circuits
# from eisy.simulation.plotting import nyquist_plot
"""
Unit Testing for "EISy As Py" File Management tools
 * Note: A significant amount of the logic and programming here involves
          reading, writing files as well as user interaction.
          How is unit-testing done for this?
"""


class TestFileManagement(unittest.TestCase):

    def test_new_config_import(self):
        """
        new_config_import will generate a prescribed configuration dictionary.
        If given a path and save=True (default), it will save that dictionary
        as a yaml file.
        if save=False, will not attempt to save and instead simply return the
        configuration dictionary.
        """
        config_dict = eisy_file_mgmt.new_config_import(save=False)
        assert isinstance(config_dict, dict), "config file is not a dictionary"
        assert isinstance(config_dict["header_meta"], dict), "header not Dict"

        # Test if it catches a bad path
        try:
            eisy_file_mgmt.new_config_import("/badpath/",
                                             save=False,
                                             interact=False,
                                             popup=False)
            raise AssertionError("Didn't catch Bad YAML config Path")
        except AssertionError:
            pass

    def test_get_config_import(self):
        """
        Get_config_import will load a configuration file from YAML file given.
        This should aelso be wrapped up in the set_config_import function,
        which is smart and will either get the file if it exists or will
        make a new one if needed.

        again, we can not use travis.ci to inspect user-interactions, so we
        must turn interact=False.

        Instead, we will check/confirm that it throws errors if given bad input

        """
        # if there is no file to grab, should error out
        try:
            config_dict = eisy_file_mgmt.get_config_import("BadPath.yaml",
                                                           interact=False)
        except AssertionError:
            pass

        # Otherwise, function should pass using defaults
        config_dict = eisy_file_mgmt.get_config_import(interact=False)

    def test_set_config_import(self):
        """

        """
        # IF you change a configuration that is not in the file, should error
        try:
            config_dict = eisy_file_mgmt.set_config_import(
                change={"new": "test"}, add_new=False)
        except AssertionError:
            pass
        # If the file does not exist, will create the file.
        # But should error out if the file name is not a .yaml
        try:
            config_dict = eisy_file_mgmt.set_config_import(
                    "badpath/config.yaml")
        except IsADirectoryError:
            pass
        assert isinstance(config_dict, dict), 'the configuration dictionary\
        should be a dictionary'

    def test_get_file_list(self):
        """

        """
        import os.path

        # Ask for list of test files in the test directory
        test_dir = "eisy/test/data/"
        files, file_path = eisy_file_mgmt.get_file_list(dir_path=test_dir,
                                                        str_has=['.'],
                                                        str_inc=['.'],
                                                        interact=False)
        assert isinstance(files, tuple), "File list must be tuple"

        assert os.path.isdir(file_path), "File Path has failed!"

        files, file_path = eisy_file_mgmt.get_file_list(dir_path=test_dir,
                                                        str_has=["sim"],
                                                        str_inc=["data"],
                                                        interact=False)

    def test_check_dir_path(self):
        dir_path = "eisy/test/data/"
        a, msg = eisy_file_mgmt.check_dir_path(dir_path,
                                               files_contain=['.csv'],
                                               n_required=1,
                                               raise_err=True)
        try:
            b, msg2, = eisy_file_mgmt.check_dir_path("badpath/")
        except AssertionError:
            pass
