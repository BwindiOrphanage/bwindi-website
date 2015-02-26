#!/usr/bin/python2
import gmail
import sys
import re
import subprocess

if not subprocess.call("git diff-files --quiet --ignore-submodules", shell=True):
    # There are unstaged git changes so don't proceed
    print("There are unstaged changes in the git repo. Auto updater will not proceed.")
    sys.exit(0)

# Emails with this subject line will be added to the website
SUBJECT_LINE_TRIGGER = "bwindi-blog-post"
POSTS_DIRECTORY_PATH = "../_posts"
DEBUG = True

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
    sys.exit()

try:
    emails = g.inbox().mail(unread=True, subject=SUBJECT_LINE_TRIGGER, prefetch=True)
    print("Read inbox succesfully.")
except:
    print("Could not read inbox.")
    sys.exit()

if len(emails) < 1:
    print("No special emails found. Exiting")
    g.logout()
    sys.exit(0)

for email in emails:
    print("Special email found.")
    print("BODY:\n" + email.body)
    timestamp = email.sent_at
    dateString = str(timestamp.date())
    # get the first sentence with a regex pattern
    # use this as the title.
    match = re.search("\s*(\w[^!.?]*)[!.?]", email.body, flags=re.MULTILINE)
    if not match:
        print("ERROR: could not parse a first sentence from the email. Quitting.")
        sys.exit()

    titleString = match.group(1).title() # title method capitalizes the first letter of each word
    titleForPostFile = dateString + '-' + re.sub("\s+", "", titleString) # remove all whitespace
    print("First sentence (used as title): " + titleString)
    print("Title for post file: " + titleForPostFile)

    restOfMessage = email.body[match.end():].strip() # remove leading and ending whitespace

    newPost = '\n'.join(["----------", 
                         "layout: post",
                         "date: " + str(timestamp),
                         "title: " + titleString,
                         "----------",
                         restOfMessage])

    print("New blog post created:\n" + newPost)

    if not DEBUG:
        email.read() # mark it as read
        filePath = POSTS_DIRECTORY_PATH + '/' + titleForPostFile + ".markdown"
        newPostFile = open(filePath, 'w')
        newPostFile.write(newPost)
        print("Wrote new post to: " + filePath)

subprocess.call("git add .", shell=True)
subprocess.call('git commit -m "AUTOMATED: add new blog posts."', shell=True)
subprocess.call('git push origin master', shell=True)

g.logout()
