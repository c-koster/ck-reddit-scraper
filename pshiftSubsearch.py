"""
This script should take as parameters a subreddit and two time stamps, then output
 a text file which can be looked over by the submission scraper.
Uses the pushshift API because praw does not support this anymore.
"""
import time
import sys
import urllib.request
import json

BASE_URL = "https://api.pushshift.io/reddit/submission/search/"

def get_submissions(sub,timeBefore,timeAfter):
    """
    Takes in a subreddit name and two dates as parameters, makes a request to
    pushshift.io -- no credentials needed here.
    """
    # build the url string
    url = BASE_URL+"?subreddit="+sub+"&sort=asc&limit=1000&sort_type=created_utc&after="+timeAfter+"&before="+timeBefore

    with urllib.request.urlopen(url) as webpage:
        contents = webpage.read().decode('utf-8') # read page

    # re-code it as a dictionary
    d = json.loads(contents)
    L = d['data']
    return L


def write_submissions(L,outfile="outfile.txt"):
    """
    Takes a list of url strings as input and writes them to an output
    file named <outfile>.
    """
    f = open(outfile,"w")
    numUrls = len(L)

    if numUrls == 0: # found 0 urls
        print("I didn't find anything.")
        return
    for url in L:
        f.write(url + '\n')
    print("wrote "+str(numUrls)+" to: " + outfile)
    return numUrls


def write_all_links(subreddit,timeAfter,timeBefore,outfile="urlList.txt"):
    """
    Used a while loop to repeatedly call get_submissions. This accomodates requests
    which contain more than 1000 links.
    """
    submissionDict = get_submissions(subreddit,timeBefore,timeAfter)
    # pull initial set of submissions
    urlList = []
    lastT = timeAfter

    # re-query after the last submission time until there are no more links
    while len(submissionDict) != 0:

        for s in submissionDict:
            urlList.append(s["full_link"]) # add the link
            lastT = s["created_utc"]
        # print("too many posts... re-querying after " + time.ctime(lastT))
        submissionDict = get_submissions(subreddit,timeBefore,str(lastT))

    n = write_submissions(urlList,outfile=outfile)
    # write all submissions --  <n> is the number of submissions written.
    return n

def get_urls(filename):
    """
    Takes as input a txt filename, and returns a heap pointer/memory list.
    """
    L = []
    f = open(filename,'r')
    for line in f:
        L.append(line.strip('\n'))
    return L
