# Guide 

## Signing in and setting up
Please use lxplus7, otherwise various macros may behave unexpectedly.
Run setupATLAS before running any job requests for condor
There are various macros with file paths that will need to be adjusted. They all use the EOS space, it may be recommended to ctrl+F for "eos" to look for and replace any filepaths.

## Submitting Jobs with Condor
To submit jobs with condor, we use the Batch system outlined here: https://batchdocs.web.cern.ch/local/submit.html
Use SubmitCondor.py to submit the jobs themselves.

### condor_evnt.sh
These hold the batch commands that each node on condor assigned to one of our jobs will run. They take parameters from an args.txt file written by either SubmitCondor.py, this is why we need to do setupATLAS before submitting jobs.

### SubmitCondor.py and SubmitCondor_og.py
The Filesystem setup is that configs represent folders holding sets of python job-options files, that have been configured to different setups that are separeted by the config folders. 

E.G for a certain analysis with SubmitCondor_og.py

100xxx may have 515520 and 515496 at their default settings

max_100xxx may have 515520 and 515496 at their maximum settings for a certain physics aspect, controlled by variables in the job options

min_100xxx may have 515520 and 515496 at their minimum settings for a certain physics aspect, controlled by variables in the job options

initial_dir and work_dir should represent this in submitCondor.py but may not in SubmitCondor_og.py, as the last time it was used may not have required separete setups of signal points... 
These will *only* send jobs to condor, to retrieve the job files after the jobs have finished runnning, see "transfer_condor.py"

To run it, write in the terminal "python SubmitCondor.py"

#### SubmitCondor.py
The settings to vary the job are:
- configs: the tags / signal points to use, which go inside the "configs" list of strings.
- n_events: the amount of events each job should have
- n_total: the amount of total events any signal point should have
- get_python_filename/filename_map: this is for linking the signal points int ID to the job options python file, the tag ID as well as their corresponding job options py file are commented out at the bottom of the macro
- any file paths 
To ensure all repeated jobs have different seeds, notice the seed for loop.
The current functionality is to create 11 jobs per tag, where all strings are correlated to the filesystem I setup. This is done specifically for an analysis task. For a more general use case, please see SubmitCondor_og.py.

#### SubmitCondor_og.py
- d_args_ISR: same functionality as get_python_filename/filename_map

### Transfer_condor.py
DUring the Submit_Condor processes, we write each job ID to a separete text file in the same directory as the Submit_Condor.py file itself, this file is called job_ids.txt.
To run it, write in the terminal "python3 transfer_condor.py"

## Job-Option editing macros
These are all designed to work on fractions of, or the entirety of the 100xxx directory within https://gitlab.cern.ch/ebusch/svj-s-channel-signal-request

### Max/Minconfigmacro.py
These belong in the directory containing the 100xxx/copy folder. Running either of these will look for a directory to match with the base_directory string in the macros, and then edit the job options for relative max/min configurations of aLund, bmqv2 and rFactqv.

### ISRFSRmacro.py
This changes the generator settings within 10 sets of job options. The setup is to have 11 directories of signal points, e.g 515502, 515502_1 ... 515502_10. This macro will iterate over _1 to _10 and change the generator settings to what they need to be.
