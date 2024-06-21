import subprocess

# Open the file with job IDs
with open("job_ids.txt", "r") as job_ids_file:
    for job_id in job_ids_file:
        job_id = job_id.strip()  # Remove any newline or whitespace
        if job_id:
            print("Transferring data for job ID: {}".format(job_id))
            # Construct the command and execute it, compatible with Python 3.6
            result = subprocess.run(["condor_transfer_data", job_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Check the result of the transfer command
            if result.returncode == 0:
                print("Data transfer successful for job ID: {}".format(job_id))
            else:
                print("Data transfer failed for job ID: {}".format(job_id))
                print("Error:", result.stderr)
