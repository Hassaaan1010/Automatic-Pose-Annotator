#!/bin/bash


# declare input and output directories for images to be numbered. 
# Output directory must be empty to avoid overwrites.

#directory paths
input_dir="/home/hassaan/Downloads/try_again_2/rgb_split_2.1/"
output_dir="/home/hassaan/Downloads/try_again_2/rgb_split_2.1/"

# Create a temporary directory for renaming
mkdir -p "$output_dir"

# Initialize counter
counter=10000

# Loop through all image files in the inp directory
for file in "$input_dir"/*; do
  # Extract the file extension
  extension="${file##*.}"

  # Rename the file with the new larger number
  # cp "$file" "$temp_dir/$counter.$extension"
  mv "$file" "$output_dir/$counter.$extension"

  # Increment the counter
  ((counter++))
done


# renumbers starting from 0
counter=0
# Loop through all image files in the directory
for file in "$input_dir"/*; do
  # Extract the file extension
  extension="${file##*.}"

  # Rename the file with the new number
  # cp "$file" "$temp_dir/$counter.$extension"
  mv "$file" "$output_dir/$counter.$extension"

  # Increment the counter
  ((counter++))
done