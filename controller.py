"""
Culton Koster

Controller/master scrape script -- make queries by calling me!
TODO:
- auth credentials should be replaced, and passed in or read from a txt file

- error handling and logging for posts that are too large, or do not exist. (use
 logging module for this)
- in logging system, compare submission.comments to number of comments actually scraped
 to determine if there are actual discrepancies...
"""
import sys
import os

import praw
import pshiftSubsearch as ps
import submissionScrape as ss


from dotenv import load_dotenv
load_dotenv() # fetch env variables from my .env file


api_key = os.environ.get("ALPHAVANTAGE_API")
# app id and secret --
c_id = os.environ.get("C_ID")
c_secret = os.environ.get("C_SECRET")
# user and pw -- also super secret ...
user = os.environ.get("USERNAME")
pw = os.environ.get("PASSWORD")

# declare file names here
treeName = 'tree.csv'
adjName = 'listfile.csv'
urlFilename = 'urls.txt'


def process_urls_tree(urls,prefix,conn):
    """
    Scrape and process comments from a url list into a tree csv.
    """
    outfile = prefix + treeName
    errorCases = []
    for to_scan in urls:
        submission = ss.scan_link(to_scan,conn)
        ss.write_tree(submission,toWrite=outfile)
    return errorCases


if __name__ == '__main__':
    if len(sys.argv) != 4:
        # print a usage statement
        print("usage: controller.py <subreddit-name> <after> <before(yyyy-mm-dd)>")
    else:
        conn =  praw.Reddit(client_id=c_id,
                         client_secret=c_secret,
                         password=pw,
                         user_agent='subreddit query by /u/c-koala',
                         username=user)

        rid = sys.argv[1] #subreddit name
        timeAfter = sys.argv[2]
        timeBefore = sys.argv[3]

        # file prefix, can change naming scheme
        prefix = rid + "<"+ timeAfter + "><" + timeBefore + ">"


        numLinks = ps.write_all_links(rid,timeAfter,timeBefore,outfile=urlFilename)
        urls = ps.get_urls(urlFilename) # get a long list of urls from requested dates
        errors = process_urls_tree(urls,prefix,conn)
