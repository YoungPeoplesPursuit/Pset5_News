# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Tina
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz



#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate



#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    def is_phrase_in(self, excerpt):
        checked = "" #creating a new string that is cleaned excerpt
        for c in excerpt:
            if c in string.punctuation:
                checked = checked + " "
            else:
                checked = checked + c.lower()
        wordlist = checked.split() #split checked into words by space
        checked_no_space = " ".join(wordlist) #excerpt with cleaned spaces
        phraselist = (self.phrase).split()

        if self.phrase not in checked_no_space:
            return False
        else:
            for e in phraselist:
                if e not in wordlist:
                    return False
            return True


# Problem 3

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)
    def evaluate(self, story):
        excerpt = story.get_title()
        return self.is_phrase_in(excerpt)

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)
    def evaluate(self, story):
        excerpt = story.get_description()
        return self.is_phrase_in(excerpt)

# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    def __init__(self, stringtime):
        format_string = "%d %b %Y %H:%M:%S"
        dateformat = datetime.strptime(stringtime, format_string)

        est_timezone = pytz.timezone('US/Eastern')  # Define EST timezone
        # To force it to be UTC-5 as implied by "EST" in the problem statement:
        est_offset = pytz.FixedOffset(-300)  # -300 minutes = -5 hours = UTC-5
        self.time = dateformat.replace(tzinfo=est_offset)  # Make it aware with a fixed UTC-5 offset

# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6

class BeforeTrigger(TimeTrigger):
    def __init__(self, stringtime):
        super().__init__(stringtime) #inherits constructor from superclass

    def evaluate(self, story):
        storytime = story.get_pubdate()
        # Convert both self.time and storytime_aware to UTC for comparison
        trigger_time_utc = self.time.astimezone(pytz.utc)
        story_time_utc = storytime.astimezone(pytz.utc)

        return story_time_utc < trigger_time_utc

class AfterTrigger(TimeTrigger):
    def __init__(self, stringtime):
        super().__init__(stringtime)

    def evaluate(self, story):
        storytime = story.get_pubdate()
        trigger_time_utc = self.time.astimezone(pytz.utc)
        story_time_utc = storytime.astimezone(pytz.utc)

        return story_time_utc > self.time

        # COMPOSITE TRIGGERS

# Problem 7

class NotTrigger(Trigger):
    def __init__(self, T):
        self.T = T
    def evaluate(self, story):
        return not (self.T).evaluate(story)
# Problem 8

class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2
    def evaluate(self, story):
        return (self.T1).evaluate(story) and (self.T2).evaluate(story)

# Problem 9

class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2
    def evaluate(self, story):
        return (self.T1).evaluate(story) or (self.T2).evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggeredList = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggeredList.append(story)
    return triggeredList



#======================
# User-Specified Triggers
#======================
# Problem 11

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # create dictionaries mapping words to functions
    triggerkeys1arg = {'TITLE': TitleTrigger, 'DESCRIPTION' : DescriptionTrigger, 'NOT' : NotTrigger, 'BEFORE' : BeforeTrigger, 'AFTER': AfterTrigger}
    triggerkeys2arg = {'AND': AndTrigger, 'OR': OrTrigger}
    triggerkeys = {} #where we store the triggers created
    addedtriggers = [] #where we add the triggers to the list to return
    for line in lines:
        linelist = line.split(',')
        if linelist[0] == 'ADD': #if is ADD simply add triggers from dictionary to list to return
            for i in range(1, len(linelist)):
                triggername = linelist[i]
                if triggername in triggerkeys:
                    addedtriggers.append(triggerkeys[triggername])
        else: #find the function corresponding to word, add triggerkeys key as trigger name and value as function with parameters plugged in
            triggername = linelist[0]
            triggertype = linelist[1]
            if triggertype in triggerkeys1arg:
                function = triggerkeys1arg[triggertype]
                triggerkeys[triggername] = function(linelist[2])
            else:
                function = triggerkeys2arg[triggertype]
                arg1 = triggerkeys[linelist[2]]
                arg2 = triggerkeys[linelist[3]]
                triggerkeys[triggername] = function(arg1, arg2)

    return addedtriggers


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Elon Musk")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("tariff")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11

        triggerlist = read_trigger_config('triggers.txt')
        triggerlist = read_trigger_config('myfeed')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

