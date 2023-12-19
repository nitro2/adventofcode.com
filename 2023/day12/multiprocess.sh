#!/bin/bash
for f in input/*.*; do
    file_name=$(basename "$f")
    python3 day12.2_multi.py "$f" > "./output/$file_name.out" &
    echo $file_name
done
wait