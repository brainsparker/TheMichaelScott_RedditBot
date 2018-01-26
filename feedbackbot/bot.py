#!/usr/bin/python
from  configparser import SafeConfigParser
import praw
import random
import logging
import time
import os

message_subject = 'Your latest post in r/Feedback'
message_body = ('Your latest post in r/Feedback has been removed because '
		'according to your comment history you have not yet contributed '
		'feedback to others. You may post in the subreddit once '
		'you have participated in the community.')

reddit_bot = praw.Reddit(user_agent=os.environ['user_agent'],
				      client_id=os.environ['client_id'],
				      client_secret=os.environ['client_secret'],
				      username=os.environ['username'],
				      password=os.environ['password'])

now = int(time.time())

for submission in reddit_bot.subreddit('feedback').new():
    submission_time = int(submission.created_utc) #or .created
    if (now - submission_time) > 600:
        break
    else:
        op = reddit_bot.submission.author
        print('OP is ' + op)
        noncontributor = True
        for comment in reddit_bot.redditor(op).comments.new(limit=None):
            print('comment subreddit : %s' % str(comment.subreddit))
            if str(comment.subreddit) == 'feedback':
                noncontributor = False
                break
        if noncontributor:
            print('User hasn\'t contributed. Removing Submission')
            reddit_bot.submission.SubmissionModeration(submission).remove()
            print('Notifying User of Submission Removal via DM')
            reddit_bot.redditor(op).message(message_subject,message_body,from_subreddit='feedback')
