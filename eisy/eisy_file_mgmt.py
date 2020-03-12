"""
WIP for testing data Import, Formatting, and then Export to SQL and/or other


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

* fseries_read_data()   Takes a file name, expected metadata config, and
                        some interaction parameters (?).
                        Reads the file, separates the metadata from the series
                        data, and calls fix_fseries on the headers.
                        (may call some smart s#!t if the parsing is difficult.)
                        Returns dfs of raw data, and 2x meta data, for the file

* fseries_fix_head()    IF the headers in the data frame are not named/ordered
                        correctly, we need to fix that.
                        Identify the columns by their headers and/or data types
                        and then rename and re-order the columns according
                        to a specific configuration. (in SQL Config doc?)
                        Returns RAW_DATA

* fseries_process_data()Takes the Raw Data, and makes some quick notes about
                        the results. Currently Work in Progress - Not sure
                        how much of this the team wants.
                        Either way, outputs this as our third type of Meta-data
                        Returns PROCESSED_DATA

* fseries_metadata()    Takes up to two meta-data dataframes
                        (One from file name, other from header), and reconciles
                        any overlap based on some configuration and sorta-smart
                        manipulation.
                        Returns EXPERIMENT_METADATA

* fseries_combinedata() Uses a Configuration file (See SQL_get_config???)
                        to combine all the data for one file into a single line
                        of a Pandas DataFrame.

                        Format such as:
                        |Serial_ID|Experiment_Metadata|raw_data|processed_data|
                        + empty spots for:
                        |noise_classify|shape_classify|experimental_feedback|


Section 3: Export All Data into SQL Database as configured
----------------------------------------------------------


* SQL_get_config()      Reads a configuration file that demonstrates how
                        the SQL server is to be set up.
                        SHOULD (?) FOLLOW STANDARD SCHEMA DESIGN RULES (?)

* SQL_setup()           Takes in instructions/configurations, and initiates
                        a new SQL database to interact with using
                        SQL Alchemy...

* SQL_dataframe()       agvfgl;mlkjgfcvx bnm,,km
                        (We're not here yet. no idea what this will actually
                        need as inputs and outputs.)



"""
# ----------------------------------------------------------------------------
# --- HARD - CODING SECTION --------------------------------------------------
# ----------------------------------------------------------------------------


config_file_location = "config/config_importer.yaml"


# ----------------------------------------------------------------------------
# --- OK. Now on to the Program!----------------------------------------------
# ----------------------------------------------------------------------------


"""
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
---SECTION 0 : Configuration Files---------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
"""


def new_config_import(config_file=config_file_location,
                      save=True, interact=False, popup=False, **change):
    """
    This function will set up a config file for data importing,
    and can be customized in many ways, depending on user interest.

    INPUT:
        config_file     : String where we can save the file, if desired.
                          if file already exists, will raise error.

        save            : Boolean, whether or not to save this file.
                          either way will return a config dictionary

        interact        : Boolean, whether to ask the user to manually submit
                          additional values to the dictionary.

        popup           : Boolean, whether interactions should use tkinter
                           input windows, or ask for input in the kernel.

        **change        : **KWARGS - User can input additional elements which
                          will be added to the dictionary

    RETURN:
        config          : Dictionary (or dataframe? pandas series?) in config

    ACTIONS:
        * Optional request for any additional arguments
        * Optional save-file (if SAVE)

    NOTE: FUNCTION IS WORK-IN-PROGRESS. For MAIN USE-CASE, currently
            require user input to be hard-coded in the initial "config"
            dictionary below. It's also an open question whether to save
            as CSV file or whether to learn/use YAML'
    """
    import yaml
    from datetime import datetime
    import os.path
    config_dir = os.path.dirname(config_file)
    config = {
            "data_dir": "data/simulation/simulation_data",
            "config_created": str(datetime.now()),
            "config_updated": None,
            "file_type": ".csv",  # just to check that the edit works
            "header_meta": {
                    "date_run": "Date:",
                    "serial_n": "Serial number:",
                    "d_source": "Data Source:",
                    "circuit_str": "Cirucit type:",
                    "circuit_detail": "Circuit elements:"
                    },
            "header_end_str": "---",
            "fdata_delim": ",",
            "fdata_head": {
                    "freq_hz":   "freq [Hz]",
                    "real_ohm":  "Re_Z [Ohm]",
                    "imag_ohm":  "Im_Z [Ohm]",
                    "totl_ohm":  "|Z| [Ohm]",
                    "phase_rad": "phase_angle [rad]",
                    }
              }
    if change:
        # Handle arguments passed directly into funciton:
        # Probably overwrite if key exists, otherwise simply
        # add to dictionary?
        print("Work in Progress. Will execute kwargs another time")
        pass

    if interact:
        # Did the user ask for an interaction? If so, how?
        if popup:
            # If the user wants a tkinter window to ask for
            # what arguments they want, then give them that?
            import tkinter
            change_interact = ""  # WIP, leave empty
        else:
            # If no popup windows, then ask in command line
            print("Please Input Config Parameters. Leave blank to finish")
            key = 'init'  # Counter (to avoid infinite loop?)
            change_str = 'test'
            while key and change_str:
                print("\n")
                key = input("Input Key:    ")
                change_str = input("Input Value:  ")
                if key and change_str:
                    # If you passed two arguments, assign the value to the key
                    # in the config dictionary
                    config[key] = change_str

    if save:
        # If instructions are to save the new config file,
        # We will use dump YAML, as suggested in class
        # But first check that the path to save exists

        if os.path.isdir(config_dir):
            pass
        else:
            # Create directory if doesn't exist
            os.mkdir(config_dir)

        # Now, save the file using yaml
        f = open(config_file, "w+")
        yaml.dump(config, f)
        f.truncate()
        f.close()

    return config


def get_config_import(config_file=config_file_location,
                      interact=False):
    """
    Simple import script, to load the YAML configuration file.
    So far it just checks that the file exists, and if it does it loads it.
    IF doesn't exist, either raises error or uses a TKinter window to ask.

    Future WIP: Test Checks to make sure that the file contains the needed
                configuration parameters that we use in our other programs.
                Namely:
                * file_dir : The directory to default load data files from
                *
                *
    """
    import yaml
    import os.path
    import tkinter
    from tkinter.filedialog import askdirectory
    if os.path.isfile(config_file):
        pass
    else:
        if interact:
            print("No Config Found! Select Config File:")
            root = tkinter.Tk()
            root.lift()
            root.focus_force()
            config_file = askdirectory(parent=root,
                                       title="Select Import Config",
                                       initialdir=os.path.abspath(config_file)
                                       )
            root.destroy()
        else:
            raise AssertionError("No Config Found at : " + config_file + '\n' +
                                 "Try Again with a different file path!")

    f = open(config_file, "r")
    config = yaml.safe_load(f)
    f.close()
    return config


def set_config_import(config_file=config_file_location,
                      change={"file_type": ".csv"}, add_new=False):
    """
    Create or Modify configuration file, used to pass new defaults
    Will import and parse the file if it exists.
    Otherwise it starts from scratch, and saves the file afterwards.
    INPUT:
        config_file :   [str] The file path and file to read as the importer.
                        In a meta-sense, this default should probably be
                        UNIFIED throughout the document. IF SO, perhaps
                        I should define this globablly at the top.
                        (Also would be easier to hard-code for users)

        change :        [dict] Open ended... A ldict of keys to edit in the
                        config file. Anything put here will overwrite the
                        existing config dictionary for that item.
                        We have the default filetype:csv here as an example

        add_new :       [BOOL] how to handle keys given to "Change" that are
                        not in the existing config file. If TRUE, will add
                        new keys to the end of the config. if FALSE, will
                        raise assertionerror - key not found.

    """
    import os.path
    from datetime import datetime
    import yaml

    if os.path.isfile(config_file):
        # Import existing Config, to be edited
        print("Importer Configuration found!")
        config = get_config_import(config_file)
    else:
        # CREATE NEW CONFIG DICT FROM SCRATCH
        print("Importer Configuration Not found! \nCreating New One...")
        config = new_config_import(save=False, interact=False)

    # Now go through every key in the change dictionary and update config
    change_keys = change.keys()
    for key in change_keys:
        if key not in config.keys():
            # How to handle a "Change" entry that isn't already in the config??
            if add_new:
                config[key] = change[key]
            else:
                raise AssertionError("Key <" + str(key) +
                                     "> is not in Config file")
        else:
            config[key] = change[key]

    # Always update config_updated timestamp, right before saving
    config["config_updated"] = str(datetime.now())
    # save_config = pd.DataFrame.from_dict(data=config) # This seems broken?
    # Not sure why the dataframe idea wasn't working, however I think we can
    #    just leave things as the dictionary.

    f = open(config_file, 'w+')
    yaml.dump(config, f)      # Save and overwrite config file
    f.truncate()              # Eliminates extra lines if file got shorter
    f.close()
    return config

# ----------------------------------------------------------------------------
# --- END OF SECTION ZERO.----------------------------------------------------
# ----------------------------------------------------------------------------
# --- NOW, IMPORT THE CONFIG FILE AND USE IT FOR THE OTHER FUNCTIONS----------
# ----------------------------------------------------------------------------

# SET is actually the Omni-importer, because it will GET if possible and NEW
#    If nothing can be found.


config = set_config_import(change={})

# We call the Config function here,
# Because it doesn't work until you have defined all the functions above...
# I think this is ok, because if there is an error and you call the edit-config
#     function, then the next time you import this file it will run again
#     with the new configuration.


"""
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
---SECTION 1 : Files to Import List   -----------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
"""


def get_file_list(dir_path=config["data_dir"],
                  str_has=['sim'], str_inc=['0001', '0002'],
                  ftype=config['file_type'],
                  interact=True):
    """
    Get a list of file paths to open, which fulfill certain criteria.
    (Alternative to single/multiselect File Dialog, or hard-coded file names
        INPUTS:
            * Path to check initially.
                (hard-coded default for now. can we globally config?)
            * Basic filter parameters, defaults just for testing now.
                str_has: AND filter (Must contain all in list)
                str_inc: OR  filter (Must contain at least one)
            * File type to check for. Default csv
            * whether to use file dialogs if the path fails, or just error out.
        OUTPUTS:
            * TUPLE of file names that pass the tests (built as list)
            * Final (successful) directory path used. (from cwd, or from base)

    """
    import os.path
    from os import listdir
    import tkinter
    from tkinter.filedialog import askdirectory
    root = tkinter.Tk()  # this will help control file dialog boxes!

    # Check if the path specified includes at least 1 file of the file type
    success, err_msg = check_dir_path(dir_path, [ftype], 1, False)

    while not success and len(dir_path):
        # If the "default" directory failed the check,
        # Either raise that error, or ask for a different directory!
        # (Will exit If you X out of the dialog, to avoid getting stuck)
        print("Bad Folder: <" + dir_path + ">   -   " +
              'Choose a new one, then Update your Config File!')
        if interact:
            root.lift()
            root.focus_force()
            dir_path = askdirectory(parent=root, title=err_msg,
                                    initialdir=dir_path)
            success, err_msg = check_dir_path(dir_path, [ftype], 1, False)
        else:
            root.destroy
            raise AssertionError(err_msg)
    else:
        print("You found a good folder at: <" + dir_path + ">")

    if not len(dir_path):
        root.destroy()
        raise AssertionError("You Closed the Dialog Window Without a Folder!")
    root.destroy()

    """
    If we've gotten this far, we found files!
    So now, we will filter the list based on the parameters given, and return
    the result as a file list to open.
    """
    # NOTE: Add File Type to File_has, so we only select that type of file
    str_has.append(ftype)

    full_dir = listdir(dir_path)
    files_wanted = []
    for file in full_dir:
        # For each file, decide if it passes
        for str_AND in str_has:
            # IF any of these fail, ignore the file.
            if str_AND in file:
                pass
            else:
                break
        else:
            # Only does this if all "Required" strings pass
            for str_OR in str_inc:
                # If ANY string is found in the file,
                # Add it to the list and then go to next file
                if str_OR in file:
                    files_wanted.append(os.path.join(dir_path, file))
                    break
                else:
                    pass
    return tuple(files_wanted), dir_path


def check_dir_path(dir_path, files_contain=['.csv'], n_required=1,
                   raise_err=False):
    """
    Check if a directory contains the files you want:
        INPUTS:
            * Path to check (required)
            * LIST of strings to check. Files must contain ALL strings to pass.
                (Default is set to look for .csv)
            * Number of successful files required to pass the test
                (Default is 1 file)
            * Failure Handling. whether to Return Failure or raise an Error.
                (Default is FALSE, which will not raise errors.)
        OUTPUTS:
            * BOOLEAN (T/F), did we find all the required files?
            * Error Message, to use in selecting a folder if we failed.
    """
    import os.path
    from os import listdir
    if os.path.isdir(dir_path):
        # First confirm that it's a directory, otherwise fail
        file_list = listdir(dir_path)
        if len(file_list) == 0:
            if raise_err:
                raise AssertionError("That Directory is Empty")
            else:
                return False, "That Directory is Empty!"
        else:
            files_found = 0
        for file in file_list:
            # Search each file name
            for str_required in files_contain:
                # To succeed, must have ALL strings in the list
                if str_required in file:
                    # If this string is in the name
                    pass  # Check the next string required
                else:
                    break  # Break out of this loop (try next file?)
            else:
                # This FOR-ELSE means the file name passed the test!
                files_found += 1  # Add 1 to found_files
                if files_found >= n_required:
                    return True, "At least "+str(n_required)+" files passed!!"
        else:
            # This FOR-ELSE means that no files passed!
            if raise_err:
                raise AssertionError(str(files_found) +
                                     " Files Passed. Needed " +
                                     str(n_required) + ".")
            else:
                return False, str(str(files_found) + " Files Passed. Needed " +
                                  str(n_required) + ".")
    else:
        if raise_err:
            raise AssertionError("This is not a Directory!")
        return False, "This Is Not a Directory"
    return False, "Something Else went Wrong? Debug..."


def ask_file_list():
    """
    Alternative to get_file_list, just makes a tkinter window and asks the user
    to select the files. Written easiy so we don't have to remember tkinter
    """
    import os.path
    import tkinter
    from tkinter.filedialog import askopenfilenames
    root = tkinter.Tk()
    files_list = askopenfilenames(multiple=True)
    root.destroy()

    return files_list, os.path.abspath(files_list[0])


"""
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
---SECTION 2 : Frequency-Series Data Import -----------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
"""


def parse_fname_meta(file):
    """
    Takes a file name and separates out any/all metadata of interest
    (Serial ID, Source, NN Tags)
    Decisions to be made: How strict to be on naming?
    This should be in the config file...
    FOR NOW: Only Impose 3 Rules:
        * UNTIL FIRST "_" is Serial ID (Expect but don't force Date-Serial#)
        * END to LAST "_" (except extension .) are CLASSIFY tags
            (separated by '-' if multiple)
        * ALL OTHERS are MetaData tags. Save these if/only/if we can match
            them to any of several metadata setup config dictionaries?
            (IGNORE FOR NOW? Just pass as a list of Meta-Tags)

        INPUTS:
            fname   :   file name to be parsed.
                    :

        RETURN:
            serial_id : UNIQUE file ID. NEED OTHER FUCNTION TO CHECK UNIQUE??
            meta_tags : All tags in the middle of the file. in Future will sort
                        and separate as per config
            class_tags: CLASSIFICATION Tags - Those used to train the model.
                        Group Discussion on what to do with these for
                        non-training data?? For now, this is then a mark
                        of training (manually checked) data.
                        BLIND files maybe should then always end with "_.csv"
                        to identify them as un-observed! Suggest to group...
    """
    import os.path

    fname = os.path.basename(file)

    serial_id = ""
    meta_tags = []
    class_tags = []

    # Now separate file based on "_" markers
    a = 0  # Copy-paste placeholder
    for b in range(len(fname)):           # Loop through the file name...
        if a == 0 and fname[b] == "_":    # When you get to the first _
            serial_id = fname[a:b]        # ----Copy the first chunk as the ID
            a = b+1                       # ----(and reassign a)
        elif fname[b] == "_":             # When you find any other mid-tag
            meta_tags.append(fname[a:b])  # -----Add it to the Meta tag list
            a = b+1                       # ----(and reassign a)
        elif fname[b] == '.':             # When you get to the file extension
            class_tags_all = fname[a:b]   # The final set is all class-tags
        else:
            pass

    # Ok, same thing, now looping class_tags and separate based on "-"
    a = 0  # Use same placeholders, to show it's the same process
    for b in range(len(class_tags_all)):
        if class_tags_all[b] == "-":      # Note this time, the "-"
            class_tags.append(class_tags_all[a:b])
            a = b+1
        else:
            pass
    else:
        # If you get to the end of string, that's one last tag
        class_tags.append(class_tags_all[a:])  # Add it to the Classify list

    # NOW for internal Unit-tags
    if not len(serial_id):
        raise AssertionError("File <" + fname + "> Has no Separators.\n" +
                             "Expected <SerialID>_<tags>_<classify>.csv")
    return serial_id, meta_tags, class_tags


def fseries_read_data(file, data_head = config["fdata_head"],
                      delim=config["fdata_delim"],
                      header_end_str=config["header_end_str"],
                      header_meta_key=config["header_meta"]):
    """
    Takes a file name, expected metadata config, and
    some interaction parameters (?).
    Reads the file, separates the metadata from the series
    data, and calls fix_fseries on the headers.
    (may call some smart s#!t if the parsing is difficult.)
    Returns dfs of raw data, and 2x meta data, for the file

        INPUTS:
            file :
            config-----

        RETURN:
            header_metadata

            fseries_data


    """
    import os.path

    import pandas as pd

    # First things first, check that the file exists.
    if not os.path.isfile(file):
        raise AssertionError(file + "Is Not a Real File. Please Check...")
    else:
        pass
    # Initialize Meta-Data dataframe
    # header_meta = pd.DataFrame(columns=header_meta_key)
    # ^^ THATS NOT FORMATTED RIGHT... RE-ASSESS CONFIG?
    # ---For Now, simply copy each key,value into an empty dataframe
    header_meta = {}

    # Next: Try to separate Header and Raw via the "header_end_str":
    h_size = 0     # Initialize header size
    pos = 0        # Counter for looping through file
    f = open(file, 'r')
    while h_size == 0:
        current_line = f.readline()
        if current_line.startswith(header_end_str):
            h_size = pos
        else:
            # Still in header (unless fail)
            # ----Thus, check if it's in the expected header
            # ---- IF so, enter it as the value in the header_meta dict/df
            key, val = pd.read_csv(file, sep=delim, skiprows=pos, nrows=1)
            # if key in header_expected
            # ^^ NOT WORKING.
            header_meta[key] = val  # Assign all key, value pairs
            pos += 1
    f.close()
    #header_meta = pd.read_csv(file, sep=delim, nrows=h_size-1)
    # header_meta.
    fseries_raw = pd.read_csv(file, sep=delim, skiprows=h_size+1)
    f.close()

    return header_meta, fseries_raw


header_meta, fseries_raw = fseries_read_data('data/simulation/simulation_data\\200308-0001_sim_one.csv')






"""
* fseries_fix_head()    IF the headers in the data frame are not named/ordered
                        correctly, we need to fix that.
                        Identify the columns by their headers and/or data types
                        and then rename and re-order the columns according
                        to a specific configuration. (in SQL Config doc?)
                        Returns RAW_DATA

* fseries_process_data()Takes the Raw Data, and makes some quick notes about
                        the results. Currently Work in Progress - Not sure
                        how much of this the team wants.
                        Either way, outputs this as our third type of Meta-data
                        Returns PROCESSED_DATA

* fseries_metadata()    Takes up to two meta-data dataframes
                        (One from file name, other from header), and reconciles
                        any overlap based on some configuration and sorta-smart
                        manipulation.
                        Returns EXPERIMENT_METADATA

* fseries_combinedata() Uses a Configuration file (See SQL_get_config???)
                        to combine all the data for one file into a single line
                        of a Pandas DataFrame.

                        Format such as:
                        |Serial_ID|Experiment_Metadata|raw_data|processed_data|
                        + empty spots for:
                        |noise_classify|shape_classify|experimental_feedback|

"""


"""
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
---SECTION 3 : Setup and Export SQL Files -------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
"""


"""
* SQL_get_config()      Reads a configuration file that demonstrates how
                        the SQL server is to be set up.
                        SHOULD (?) FOLLOW STANDARD SCHEMA DESIGN RULES (?)

* SQL_setup()           Takes in instructions/configurations, and initiates
                        a new SQL database to interact with using
                        SQL Alchemy...

* SQL_dataframe()       agvfgl;mlkjgfcvx bnm,,km
                        (We're not here yet. no idea what this will actually
                        need as inputs and outputs.)
"""



















