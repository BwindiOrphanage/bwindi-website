#!/usr/bin/python2
import gmail
import sys
import re

# Emails with this subject line will be added to the website
SUBJECT_LINE_TRIGGER = "bwindi-blog-post"
POSTS_DIRECTORY_PATH = "_posts"
DEBUG = False

if len(sys.argv) < 3:
    print("Usage: email_update USERNAME PASSWORD")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

try:
    g = gmail.login(username, password)
    print("Logged in to gmail account")
except:
    print("Could not login to gmail account.")
    sys.exit(1)

try:
    emails = g.inbox().mail(unread=True, subject=SUBJECT_LINE_TRIGGER, prefetch=True)
    print("Read inbox succesfully.")
except:
    print("Could not read inbox.")
    sys.exit(1)

if len(emails) < 1:
    print("No special emails found. Exiting")
    g.logout()
    sys.exit(1)

for email in emails:
    print("Special email found.")
    bodyText = email.body.strip()
    print("Body text:\n" + bodyText)
    timestamp = email.sent_at
    dateString = str(timestamp.date())

    # get the first sentence with a regex pattern
    # use this as the title.
    match = re.search("\s*(\w[^!.?]*)[!.?]", bodyText)
    if not match:
        print("ERROR: could not parse a first sentence from the email. Quitting.")
        sys.exit(1)

    titleString = match.group(1).title() # title method capitalizes the first letter of each word
    titleForPostFile = dateString + '-' + re.sub("\s+", "", titleString) # remove all whitespace
    print("First sentence (used as title): " + titleString)
    print("Title for post file: " + titleForPostFile)

    restOfMessage = bodyText[match.end():].lstrip() # remove leading whitespace if there is any

    newPost = '\n'.join(["---", 
                         "layout: post",
                         "date: " + str(timestamp),
                         'title: "' + titleString + '"',
                         "---",
                         restOfMessage])

    print("New blog post created:\n" + newPost)

    if not DEBUG:
        email.read() # mark it as read
        filePath = POSTS_DIRECTORY_PATH + '/' + titleForPostFile + ".markdown"
        newPostFile = open(filePath, 'w')
        newPostFile.write(newPost)
        print("Wrote new post to: " + filePath)

g.logout()
sys.exit(0)
