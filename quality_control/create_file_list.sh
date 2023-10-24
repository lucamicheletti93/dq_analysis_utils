#!/bin/bash
period="LHC23zzh"
run=544116
pass="cpass0"

alien_path="alien:///alice/data/2023/${period}/${run}/${pass}"
ao2d_path="AO2D.root"
output_file="input_data_${period}_${run}.txt"

file_list=($(alien_find $alien_path $ao2d_path))

for ((i=0; i<${#file_list[@]}; i++))
do
    file_list[$i]="alien://${file_list[$i]}"
done

if [ ${#file_list[@]} -gt 0 ]; then
    echo "${file_list[0]}" > "$output_file"
fi

for ((i=1; i<${#file_list[@]}; i++))
do
    echo "${file_list[$i]}" >> "$output_file"
done