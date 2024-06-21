# Configuration sets and directory prefixes
configurations = []
configs = ["a515503","a515506","a515507","a515510","a515519","a515522"]
run_ids = ["515499_1",  "515499_10",  "515499_2",  "515499_3",  "515499_4",  "515499_5",  "515499_6",  "515499_7",  "515499_8",  "515499_9"]

# Base directories for inputs and outputs (adjust as necessary)
input_base_path = '/eos/user/s/svaljee/svj-s-channel-signal-request/condor/copy_100xxx'
output_base_path = '/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/'

# Constructing the command lines
commands = []

for bigfolder in configs:
    for i in range(0,11):
        for j in range(1,6):
            if i == 0:
                folder = bigfolder[1:]
            else:
                folder = f"{bigfolder[1:]}_{i}"
            input_dir = f"{input_base_path}/{bigfolder}/{folder}/"
            output_dir = f"{output_base_path}/{bigfolder}/{folder}/"

            input_file = f"DAOD_TRUTH1.{folder}.{j}.root"
            output_file = f"hist.{folder}.{j}.root"

            command = f"TruthDerivationTester --input {input_dir + input_file} --output {output_dir + output_file} --nevents -1"
            commands.append(command)

# Output the commands
for cmd in commands:
    print(cmd)
