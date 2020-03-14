[![Build Status](https://travis-ci.org/EISy-as-Py/eisy.svg?branch=master)](https://travis-ci.org/EISy-as-Py/eisy)

# EISy-as-Py
UW DIRECT DataScience Project, to Import/Process/Store/Report Data related to Electrochemical Impedance Measurements
**For further Information, Background, Plans, and Future goals, [CHECK THE WIKI!](https://github.com/EISy-as-Py/EISy-as-Py/wiki)**

<img src=https://github.com/EISy-as-Py/eisy/blob/master/doc/project_management/misc_design/Logo3_square.PNG width=400 p align="right">

__**Readme Contents:**__
 * *"Da Rules"*
 * *GIT Folder Structure*
 * *Capabilities and Tutorials*
 * *Current Branches & WIP*
 * *Check the Wiki*

## "Da Rules" (WIP)
 * Discuss as group
 * Try not to Collaborate in Jupyter (it's a mess) - Only use your PERSONAL notebooks, And/Or claim it in a meeting!
 * DO collaborate in .py files! Open them in Spyder if you're cool! (Or Atom if you're a nerd). Or vim if you're evil. 
 * Have fun!! 
 * Have a beer! *(But don't commit-push with a beer!)*

## GIT Folder Structure
 * Main Folder
     * standard files (gitignore, readme, etc)
     * Finished/ Tested Tutorials (Jupyter ok)
     * Core files? TBD? (Folder rules are a future lecture)
 * Data
     * SOME raw data files (only as examples) 
     * SOME mid-data files (meta and images?)
     * SOME output data (again, examples to use)
     * ReadMe / Config instructions on connecting to the Drive (?) to access ALL DA DATA
 * Planning 
     * Project Plan Docs, notes
     * Images and ideas
     * WIP or other Non-essential notebooks?
 * WIP_<*ProjectName*>
     * New Folders as Required, especially for Work - In - Progress files. (Call them /WIP_whatever/)
     * Can contain anything you want, but try and keep it organized! 
     * We may have to do a bunch of re-organization later... Talk to DBeck if that's a good idea. 

## Successes and Capabilities
 * **TBD LoL** We don't have those yet!
 * Actually, we have done some good investigations of PyEIS and ImpedancePy, the two big existing EIS Tools on GitHub!
 * We have a funny team image. we should make a better version and put it on github!
 * I drew a very pretty GUI (Just in time to decide we want a more online version... Fine... I suppose.) 
 
## WIP Items and Branches
 * __Data Generation and Modeling__: Branch "NewData" :
     * Maria and Moeez are focusing on getting us data to use, and making sure it's tagged with the proper metadata so we can train using it
     * They're using both Impedance.py and PyEIS to start, generating well modeled data to use
     * Next they'll use Real + Nonlinear data *(as available? Dan+Victor only really have raw T*I*V data so we'd need to filter ALL of it (but maybe it wont be too bad?).* 
     * Another Later test-item will be to aquire or synthesize "Bad Data" which in various ways we want to catch and either flag or reject.
     
 * __Neural Network Classifying__: Branch "Classify" :
      * Current Milestone: establish a pseudo code on importing image file using pillow and makesure we have ongoing image library.
     * Create a pseudo code on image processing/training using library. 
     * Mihyun and Jo are doing the massive research work of setting up a Neural Network Framework, which we can then use to train a model to distinguish or classify the incoming NewData. This will be a big task that once they're set up, they'll teach us to help them and we'll probably make this into NEW branches! 
     * First classify task is to identify Noisy or other failed test (AKA: Researcher Must Re-Do - Possibly with Feedback re WHY)
     * Second classify task is to identify the "Type" of data/test (AKA: Resistor? Simple RC? Battery? FuelCell?)
     * Third classify task (Optional) is to judge the quality of the results (AKA: Good/Bad battery compared to most?)
     
 * __Data + Developer + User Integration__: Branch "DataBase" : 
     * David is working on Docs-API to Python setups, so we can directly(ish?) use data from the cloud and store results there
     * There can be a team effort to sync up our various data importer work/ideas, since we've done some of that separately
     * Then we'll make sure everyone can access data the way they want it, and we can store Raw + MetaData + Results together
     * Then we'll work on SQL to do exactly-ish that^ (Followed by some sort of user interface)
     
## [CHECK THE WIKI:](https://github.com/EISy-as-Py/EISy-as-Py/wiki)
Like I said, why are you using a markdown readme for planning communication? This should be Instructions, not a planning sheet!
 
