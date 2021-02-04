"""
Set of functions which outputs post from a specific sub-reddit between
 two time stamps -- in either adjList or tree structure.
"""
import praw
import csv

# test functions -- these can be called on lists of top level comments, not submissions.
def level_order_print(L):
    """
    Used a while loop and a queue for level-order write
    """
    count = 0
    while len(L) != 0: # while queue isn't empty
        t = L[0]
        L = L[1:]
        # dequeue
        print(t.body)
        L.extend(t.replies)
        count += 1
    print("------\ndone, printed " + str(count) + " comments")


def depth_print(L):
    """
    Uses a while loop and queue, paired with a recursive 'comment-write function'
    """
    comment_count = 0
    while len(L) != 0: # while queue isn't empty
        t = L[0]
        L = L[1:]
        # dequeue
        print(str(t.body).replace("\n", " "))
        comment_count +=1
        for r in t.replies:
            comment_count += reply_print(r,1)

def reply_print(r,level):
    """
    Recursive helper to ordered print (depth first).
    """
    count = 1
    print(level*'-' + str(r.body).replace("\n", " "))
    if len(r.replies) != 0: # recursive case
        for c in r.replies:
            count += reply_print(c,level+1)
    return count


# these functions write comments to a csv file --
def write_tree(submission,toWrite="treefile.csv"):
    """
    Write a CSV with a hierarchical tree-structure.
    Uses a list of 'childid' with '/' character for delimiting.

    format:
    id,childIdList,score,level,text
    """
    L = submission.comments
    numLines = 0
    root_ids = ''
    with open(toWrite,'a') as file:

        f = csv.writer(file)
        while len(L) != 0:
            t = L[0]
            L = L[1:]
            addToRoot = '/' + t.id
            root_ids += addToRoot
            children = getKids(t)
            f.writerow([t.id,children,t.score,0,t.body])
            numLines += 1
            for reply in t.replies:
                numLines += r_write_tree(reply,1,f)
        f.writerow([submission.id,root_ids,submission.score,'s',submission.title])

    #print("done, wrote " + str(numLines) + " lines to " + toWrite)
    return numLines


def r_write_tree(reply,level,f):
    """
    Helper method to write replies recursively.
    """
    numComments = 1
    children = getKids(reply)
    f.writerow([reply.id,children,reply.score,level,reply.body])
    if len(reply.replies) != 0: # recursive case
        for r in reply.replies:
            numComments += r_write_tree(r, level+1,f)
    return numComments


def getKids(comment):
    """
    Return a formatted string to represent all children of a comment.
     (Returns a blank string if empty.)
    """
    s = ''
    for i in comment.replies:
        s+= '/' + i.id
    return s


def write_adj(submission,toWrite='listfile.csv'):
    """
    Writes a csv with a hierarrchical adjacency list infrastructure.
    Uses a 'parentid' system.

    format:
    id,parentid,score,level,text
    """
    L = submission.comments
    numLines = 0
    with open(toWrite,'w') as file:
        f = csv.writer(file)
        # write header and text.
        #f.writerow(["id","parentid","score","level","text"])
        f.writerow([submission.id,'s',submission.score,'s',submission.title])
        while len(L) != 0:
            t = L[0]
            L = L[1:]
            #dequeue
            f.writerow([t.id,t.parent_id,t.score,0,t.body])
            numLines += 1
            for reply in t.replies:
                numLines += r_write_adj(reply,1,f)
    # print("done, wrote "+ str(numLines)+ " lines to " + toWrite)
    return numLines

def r_write_adj(reply,level,f):
    """
    Recursive helper function for adjacency write.
    """
    numComments = 1
    f.writerow([reply.id,reply.parent_id,reply.score,level,reply.body])
    if len(reply.replies) != 0: # recursive case
        for r in reply.replies:
            numComments += r_write_adj(r, level+1,f)
    return numComments

# scans a link
def scan_link(to_scan,conn): # pass url and connection object
    """
    Takes a url and connection object as input, and returns a comment-extended
     "submission" class. This can be outputted/printed by calling other functions in this file
    """
    submission = conn.submission(url=to_scan)
    submission.comments.replace_more(limit=None)
    return submission
