#!/bin/bash

# Iterate over each of the main folders
for folder in a515503 a515506 a515507 a515510 a515519 a515522; do
    echo "Entering $folder"
    cd $folder

    # Iterate over each subfolder within the main folder
    for subfolder in *; do
        echo "Combining files in $subfolder"
        cd $subfolder

        # Use hadd to combine all ROOT files in this subdirectory
        hadd -f combined_hist_$subfolder.root hist.$subfolder.*.root

        cd ..  # Return to the parent directory
    done

    cd ..  # Return to the initial directory containing all the aXXXXXX folders
done

echo "All files combined successfully."
