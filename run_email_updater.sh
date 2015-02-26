#!/bin/bash
if git diff-index --quiet HEAD --; then
    # no changes
    echo "No local changes in repo... Continuing."
    python2 email_updater.py $GMAIL_USERNAME $GMAIL_PASSWORD
    git add .
    git commit -m "AUTOMATED: Adding new blog post files."
    git push origin gh-pages
    if [ $? -eq 0 ];
        echo "Commit successful."
        exit 0
    else
        echo "Commit not successful."
        exit 1
    fi
else
    # changes
    echo "Changes present in repo, not continuing."
    exit 1
fi
