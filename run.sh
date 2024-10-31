#!/bin/env bash

FOLDER="./build/"

if [[ ! -d "$FOLDER" ]]; then
    echo "Directory does not exist."
    exit 1
fi

file_list=()

# Read the file names into the array
while IFS= read -r file; do
    file_list+=("$(basename $file)")
done < <(ls -1 "$FOLDER")

if [[ ${#file_list[@]} -eq 0 ]]; then
    echo "No files found in the directory."
    exit 0
fi

echo "Select a file from the list:"
for i in "${!file_list[@]}"; do
    echo "$((i + 1)): ${file_list[i]}"
done

read -p "Enter the number of the file you want to select: " file_number

# Validate the input
if [[ ! "$file_number" =~ ^[0-9]+$ ]] || [[ "$file_number" -lt 1 ]] || [[ "$file_number" -gt ${#file_list[@]} ]]; then
    echo "Invalid selection."
    exit 1
fi

selected_file="${file_list[$((file_number - 1))]}"

echo "Executing $selected_file ..."

./build/$selected_file


