import os

# Parameters and lines to add
parameters = [2, 0.2, 2]
lines_to_add = [
    f'genSeq.Pythia8.Commands+=["HiddenValley:aLund = {parameters[0]}"]',
    f'genSeq.Pythia8.Commands+=["HiddenValley:bmqv2 = {parameters[1]}"]',
    f'genSeq.Pythia8.Commands+=["HiddenValley:rFactqv = {parameters[2]}"]'
]

# Base directory
base_directory = "max_100xxx/"

# Directory numbers
directories = [509962, 509963, 509964, 509965, 509966, 509967, 509968, 509969, 509970, 509971,
               515479, 515480, 515481, 515482, 515483, 515484, 515485, 515486, 515487, 515488,
               515489, 515490, 515491, 515492, 515493, 515494, 515495, 515496, 515497, 515498,
               515499, 515500, 515501, 515502, 515503, 515504, 515505, 515506, 515507, 515508,
               515509, 515510, 515511, 515512, 515513, 515514, 515515, 515516, 515517, 515518,
               515519, 515520, 515521, 515522]

for dir_num in directories:
    dir_path = os.path.join(base_directory, str(dir_num))
    job_options_files = [f for f in os.listdir(dir_path) if f.endswith('.py')]
    
    for job_file in job_options_files:
        full_path = os.path.join(dir_path, job_file)
        
        with open(full_path, 'r') as file:
            lines = file.readlines()
        
        insert_index = None
        for index, line in enumerate(lines):
            if '4900101:mWidth = 0.2' in line:
                insert_index = index
                break
        
        # Check if the lines to be added already exist
        already_exists = all(any(line_to_add in line for line in lines) for line_to_add in lines_to_add)
        
        if insert_index is not None and not already_exists:
            for line_to_add in reversed(lines_to_add):
                lines.insert(insert_index, line_to_add + '\n')
            
            with open(full_path, 'w') as file:
                file.writelines(lines)
