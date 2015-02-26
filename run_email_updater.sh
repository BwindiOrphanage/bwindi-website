#!/bin/bash
if git diff-index --quiet HEAD --; then
    # no changes
    echo "No local changes in repo... Continuing."
    python2 email_updater.py $GMAIL_USERNAME $GMAIL_PASSWORD
    git add .
    git commit -m "AUTOMATED: Adding new blog post files."
    git push origin master
    exit 0
else
    # changes
    echo "Changes present in repo, not continuing."
    exit 1
fi
