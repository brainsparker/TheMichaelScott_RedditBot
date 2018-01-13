#!/usr/bin/python
from  configparser import SafeConfigParser
import praw
import random
import logging
import time

logging.basicConfig(filename="simplelog.log",  format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO)

reddit_bot = praw.Reddit(user_agent=os.environ['user_agent'],
				      client_id=os.environ['client_id'],
				      client_secret=os.environ['client_secret'],
				      username=os.environ['username'],
				      password=os.environ['password'])


inapprops = list(open('phrases.txt'))
now = int(time.time())
comments = reddit_bot.get_comments('test') #reddit_bot.get_comments('DunderMifflin')
for c in comments:
    comment_time = int(c.created_utc)
    if (now - comment_time) > 3600:
        continue
    else:
        for saying in inapprops:
            if saying in c.body.lower():
                #Reply to user
                c.reply("That's what she said!")
                #Log details
                what_user = str(c.author)
                what_comment = str(c.body)
                cid = str(c.id)
                logging.info('Replied to: ' +what_user +"'s \ncomment: '"+what_comment+"' \nwith comment id: "+ cid)
                break
