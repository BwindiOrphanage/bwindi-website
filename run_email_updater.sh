#!/bin/bash

if git diff-index --quiet HEAD --; then
    echo "There are local changes!"    
fi
