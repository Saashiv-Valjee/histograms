import os

# Base directory where the subdirectories are located
base_dir = '/eos/user/s/svaljee/svj-s-channel-signal-request/condor/copy_100xxx'

# Variants mapping based on folder suffixes
variants = {
    '1': 'Var1Up', '2': 'Var1Down',
    '3': 'Var2Up', '4': 'Var2Down',
    '5': 'Var3aUp', '6': 'Var3aDown',
    '7': 'Var3bUp', '8': 'Var3bDown',
    '9': 'Var3cUp', '10': 'Var3cDown'
}

# Loop through the directory numbers
for i in range(1, 11):
    dir_path = os.path.join(base_dir, f'515502_{i}')
    variant = variants[str(i)]
    print(f"Checking directory: {dir_path}")

    # Check if the directory exists
    if os.path.isdir(dir_path):
        print(f"Found directory: {dir_path}")
        # Loop through each Python file in the directory
        for filename in os.listdir(dir_path):
            if filename.endswith('.py'):
                file_path = os.path.join(dir_path, filename)
                print(f"Processing file: {file_path}")

                # Read the content of the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Modify the specific line
                with open(file_path, 'w') as file:
                    for line in lines:
                        if 'Pythia8_A14_NNPDF23LO_Var1Down_EvtGen_Common.py' in line:
                            print(f"Original line: {line.strip()}")
                            line = line.replace('Pythia8_A14_NNPDF23LO_Var1Down_EvtGen_Common.py',
                                                f'Pythia8_A14_NNPDF23LO_{variant}_EvtGen_Common.py')
                            print(f"Modified line: {line.strip()}")
                        file.write(line)
    else:
        print(f"Directory {dir_path} does not exist.")
