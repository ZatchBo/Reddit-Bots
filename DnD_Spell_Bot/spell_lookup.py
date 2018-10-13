
import os
import atexit
import praw
import re
import time
from spells import spell_list

try:
    import cPickle as pickle
except:
    import pickle

pkl_file = "seen.pkl"
seen_posts = set()

# Load the seen posts
# if os.path.isfile(pkl_file):
#     with open(pkl_file, 'rb') as fp:
#         seen_posts = pickle.load(fp)
# Write out seen comments
@atexit.register
def write_seen_posts():
    with open(pkl_file, 'wb') as fp:
        pickle.dump(seen_posts, fp)


reddit = praw.Reddit('spellbot-script')
subreddit = reddit.subreddit('DnD')
test_subreddit = reddit.subreddit('pythonforengineers')


url_prefix = "http://forgottenrealms.wikia.com/wiki/"
comment_pre = "I noticed some spells in your post, here are some links!\n\n"
comment_post = "^(I am a bot, still in very early testing.  I'm pretty slow for now, I can only post once every 10 minutes.)"



for post in subreddit.new(limit=25):
    # Don't operate on the same post twice
    if post.id not in seen_posts:
        # Add to the list of posts to ignore
        seen_posts.add(post.id)

        reply_list = []
        comment_links = ''

        # Scan for spell names
        # TODO - better way to do this?
        for spell in spell_list:
            if re.search(spell, post.selftext):
                # Got a hit, add to the list of things to link to
                reply_list.append(spell)

        if len(reply_list) > 0:
            for spell in reply_list:
                comment_links = comment_links + "["+ spell +"]("+ url_prefix + spell +")\n\n"
            comment = comment_pre + comment_links + comment_post

            # Print for debug
            print("About to reply to post " + post.id  + ": "+ post.title + "\n" + post.selftext)
            print("Comment: " + comment)
            print("----------------------------------------------------------")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("----------------------------------------------------------")

            #post.reply(comment)
            # Sleep for a 10 min to stay good
            #time.sleep(60*10)

            # DEBUG
            for test_post in test_subreddit.new(limit=1):
                x = post.title +"\n\n"+ post.selftext +"\n\n"
                x = x+ "----------------------------------------------------------\n\n"
                x = x+ "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"
                x = x+ "----------------------------------------------------------\n\n"
                x = x+ comment
                test_post.reply(x)
                time.sleep(60*10)


write_seen_posts()