#!/bin/bash
for f in *.png; do
    mv -- "$f" "icon$i.png"
    i=$((i+1))
done
