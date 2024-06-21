from __future__ import with_statement, print_function
import numpy as np 
import os
import glob
import argparse
from subprocess import check_output
import re

d_args_debug = {
515499:'mc.MGPy8EG_SVJSChan2j_2000_2.py'}



def get_python_filename(param):
    # Dictionary mapping 515 codes to specific filenames
    param = int(param)
    filename_map = {
        515503: 'mc.MGPy8EG_SVJSChan2j_2500_2.py',
        515506: 'mc.MGPy8EG_SVJSChan2j_2500_8.py',
        515507: 'mc.MGPy8EG_SVJSChan2j_3000_2.py',
        515510: 'mc.MGPy8EG_SVJSChan2j_3000_8.py',
        515519: 'mc.MGPy8EG_SVJSChan2j_5000_2.py',
        515522: 'mc.MGPy8EG_SVJSChan2j_5000_8.py'
    }

    # Check if the parameter is in the dictionary and return the corresponding filename
    if param in filename_map:
        return filename_map[param]
    else:
        return "Code not found."

d_args_chosen = {
515499:'mc.MGPy8EG_SVJSChan2j_2000_2.py',
515502:'mc.MGPy8EG_SVJSChan2j_2000_8.py',
515519:'mc.MGPy8EG_SVJSChan2j_5000_2.py',
515522:'mc.MGPy8EG_SVJSChan2j_5000_8.py'
}

#-------------------------------------------------------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  with open("job_ids.txt", "w") as job_ids_file:
    pass
  configs = ["a515503","a515506","a515507","a515510","a515519","a515522"]
  n_offset = 1
  n_events = 25000 #10000
  n_total = 50000
  n_reps = (n_total/n_events) + n_offset

  for seed in range(n_offset,int(n_reps)):
    print('------')
    for config in configs:  
      print('----')
      for i in range(0,11): # 11 variations per folder
        if i == 0:
           numName = config[1:]
        else:
           tag = config[1:]
           numName = tag+"_"+str(i)
        print('--')
        seed = str(seed)
        # SUBMIT HERE
        print("SUBMITTING: input; {0} - {1} for event count: {2} rep: {3}".format(config, numName, n_events, seed))
        args = open("args.txt","write")
        os.system("echo '"+numName+" "+str(n_events)+" "+seed+"' >>  args.txt")
        args.close()
        open("submit.sub","write")

        os.system("echo '#!/bin/bash' >> submit.sub")
        os.system("echo 'executable            = condor_evnt.sh' >> submit.sub") ##expand here to PC 
        os.system("echo 'output                = outlogs.out' >> submit.sub")
        os.system("echo 'error                 = errlogs.err' >> submit.sub")
        os.system("echo 'log                   = logs.log' >> submit.sub")
        os.system("echo 'universe         = vanilla' >> submit.sub")
        os.system("echo 'requirements = (OpSysAndVer =?= \"CentOS7\")' >> submit.sub")
        os.system("echo 'getenv           = True' >> submit.sub")
        os.system("echo 'Rank            = Mips' >> submit.sub")
        os.system("echo '+JobFlavour	= \"workday\"' >> submit.sub")
        os.system("echo '' >> submit.sub")
        os.system("echo 'should_transfer_files = YES' >> submit.sub")
        os.system("echo 'when_to_transfer_output = ON_EXIT' >> submit.sub")
        #os.system("echo 'initialdir = /afs/cern.ch/work/e/ebusch/public/SVJ/signal_request/condor/"+numName+"' >> submit.sub")
        os.system("echo 'initialdir = /eos/user/s/svaljee/svj-s-channel-signal-request/condor/copy_100xxx/"+config+"/"+numName+"' >> submit.sub")
        #os.system("echo 'sampledir = /nevis/xenia/data/users/jgonski/xbb/Xbb_merged_samples/0121_PCJKDL1r' >> submit.sub")
        os.system("echo 'workdir = /eos/user/s/svaljee/svj-s-channel-signal-request/condor/' >> submit.sub")
        pyfile = get_python_filename(config[1:])
        print(pyfile)
        os.system("echo 'transfer_input_files = $(workdir)/condor_evnt.sh, $(workdir)/copy_100xxx/"+config+"/"+numName+"/"+pyfile+"' >> submit.sub")
        os.system("echo 'transfer_output_files =DAOD_TRUTH1."+numName+"."+seed+".root'>> submit.sub")
        print("/eos/user/s/svaljee/svj-s-channel-signal-request/condor/copy_100xxx/"+config+"/"+numName+"/"+pyfile+"")
        os.system("echo 'queue arguments from args.txt' >> submit.sub")
        submit_output = check_output(["condor_submit", "-spool", "submit.sub"])
        submit_output = submit_output.decode('utf-8')
        job_id_search = re.search(r'submitted to cluster (\d+)', submit_output)
        if job_id_search:
            job_id = job_id_search.group(1)
            print("Job ID:", job_id)

            with open("job_ids.txt", "a") as job_ids_file:
                job_ids_file.write(job_id + "\n")
        else:
            print("Failed to extract Job ID from condor_submit output")
        #time.sleep(.2)
        
        #open('submit.sub', 'w').close()

      print("DONE SUBMITTING... ")


# d_args ={
# 509962:"mc.MGPy8EG_SVJSChan2j_500_0.py",
# 509963:"mc.MGPy8EG_SVJSChan2j_500_10.py",
# 509964:"mc.MGPy8EG_SVJSChan2j_1500_0.py",
# 509965:"mc.MGPy8EG_SVJSChan2j_1500_10.py",
# 509966:"mc.MGPy8EG_SVJSChan2j_2000_0.py",
# 509967:"mc.MGPy8EG_SVJSChan2j_2000_10.py",
# 509968:"mc.MGPy8EG_SVJSChan2j_3000_0.py",
# 509969:"mc.MGPy8EG_SVJSChan2j_3000_10.py",
# 509970:"mc.MGPy8EG_SVJSChan2j_5000_0.py",
# 509971:"mc.MGPy8EG_SVJSChan2j_5000_10.py",
# 515479:"mc.MGPy8EG_SVJSChan2j_500_2.py",
# 515480:"mc.MGPy8EG_SVJSChan2j_500_4.py",
# 515481:"mc.MGPy8EG_SVJSChan2j_500_6.py",
# 515482:"mc.MGPy8EG_SVJSChan2j_500_8.py",
# 515483:"mc.MGPy8EG_SVJSChan2j_750_2.py",
# 515484:"mc.MGPy8EG_SVJSChan2j_750_4.py",
# 515485:"mc.MGPy8EG_SVJSChan2j_750_6.py",
# 515486:"mc.MGPy8EG_SVJSChan2j_750_8.py",
# 515487:"mc.MGPy8EG_SVJSChan2j_1000_2.py",
# 515488:"mc.MGPy8EG_SVJSChan2j_1000_4.py",
# 515489:"mc.MGPy8EG_SVJSChan2j_1000_6.py",
# 515490:"mc.MGPy8EG_SVJSChan2j_1000_8.py",
# 515491:"mc.MGPy8EG_SVJSChan2j_1250_2.py",
# 515492:"mc.MGPy8EG_SVJSChan2j_1250_4.py",
# 515493:"mc.MGPy8EG_SVJSChan2j_1250_6.py",
# 515494:"mc.MGPy8EG_SVJSChan2j_1250_8.py",
# 515495:"mc.MGPy8EG_SVJSChan2j_1500_2.py",
# 515496:"mc.MGPy8EG_SVJSChan2j_1500_4.py",
# 515497:"mc.MGPy8EG_SVJSChan2j_1500_6.py",
# 515498:"mc.MGPy8EG_SVJSChan2j_1500_8.py",
# 515499:"mc.MGPy8EG_SVJSChan2j_2000_2.py",
# 515500:"mc.MGPy8EG_SVJSChan2j_2000_4.py",
# 515501:"mc.MGPy8EG_SVJSChan2j_2000_6.py",
# 515502:"mc.MGPy8EG_SVJSChan2j_2000_8.py",
# 515503:"mc.MGPy8EG_SVJSChan2j_2500_2.py",
# 515504:"mc.MGPy8EG_SVJSChan2j_2500_4.py",
# 515505:"mc.MGPy8EG_SVJSChan2j_2500_6.py",
# 515506:"mc.MGPy8EG_SVJSChan2j_2500_8.py",
# 515507:"mc.MGPy8EG_SVJSChan2j_3000_2.py",
# 515508:"mc.MGPy8EG_SVJSChan2j_3000_4.py",
# 515509:"mc.MGPy8EG_SVJSChan2j_3000_6.py",
# 515510:"mc.MGPy8EG_SVJSChan2j_3000_8.py",
# 515511:"mc.MGPy8EG_SVJSChan2j_3500_2.py",
# 515512:"mc.MGPy8EG_SVJSChan2j_3500_4.py",
# 515513:"mc.MGPy8EG_SVJSChan2j_3500_6.py",
# 515514:"mc.MGPy8EG_SVJSChan2j_3500_8.py",
# 515515:"mc.MGPy8EG_SVJSChan2j_4000_2.py",
# 515516:"mc.MGPy8EG_SVJSChan2j_4000_4.py",
# 515517:"mc.MGPy8EG_SVJSChan2j_4000_6.py",
# 515518:"mc.MGPy8EG_SVJSChan2j_4000_8.py",
# 515519:"mc.MGPy8EG_SVJSChan2j_5000_2.py",
# 515520:"mc.MGPy8EG_SVJSChan2j_5000_4.py",
# 515521:"mc.MGPy8EG_SVJSChan2j_5000_6.py",
# 515522:"mc.MGPy8EG_SVJSChan2j_5000_8.py"
# }