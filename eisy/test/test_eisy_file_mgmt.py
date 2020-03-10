"""
DOC MASTER STRING Copied from eisy_file_mgmt.py
on 2020-03-10 at 1PM


Test File, to be run in order to test/confirm functionality of
EISy file management tools.

LIST AND DESCRIPTION of FUNCTIONS TO BE TESTED:
-------------------------------------------------------------------------------
Section 0: Importer Configuration File
--------------------------------------
* new_config_import()   Takes an optional/default file path and writes a new
                        configuration file in that location, with additional
                        optional inputs. The basic config file format is
                        HARD-CODED here, and can be edited as we want.
                        Optionally (default TRUE) will save the new file

* get_config_import()   Takes a config file path and loads the file if exists

* set_config_import()   Takes a config file path and dictionary of changes.
                        Either uploads the existing file in that path, or
                        creates a new one using the above functions.
                        Changes (and/or adds, optionally) the keys given,
                        and re-saves the config file.

NOTE:   To make use of Configuration codes, will call set_config_import()
        BEFORE we define other functions, so that their DEFAULT Values
        can be set according to the configuration files.
        This may or may not be kosher... I'm honestly not sure.


Section 1: Getting List of Files
--------------------------------
* get_file_list()       Takes a directory and filter parameters.
                        Returns atuple of all files in the directory
                        that match the filter parameters.

* check_dir_path()      Takes a directory and a single "AND-filter."
                        Passes if a certain number (parameter n) of files in
                        the directory contain the filter parameter.

* ask_file_list()       Simpler solution. Uses tkinter window to ask user to
                        multiselect files to be imported.


Section 2: Import F-Series Data Files (and Process Meta-Data)
-------------------------------------------------------------
* parse_fname_meta()    Takes a file name and separates out any/all metadata
                        of interest (Serial ID, Source, NN Tags)

* read_fseries_data()   Takes a file name, expected metadata information, and
                        some interaction parameters (?)
                        Reads the file,

"""

import os
import unittest

import eisy_as_py


data_path = os.path.join(eisy_as_py.__path__[0], 'data')


class test_File_Management(unittest.TestCase):

    def test_file_management(self):
        """
        Testing the stuff being tested
        """
        print("look mom, I ran a test")
        print(data_path)
