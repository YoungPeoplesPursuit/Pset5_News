PSet5: RSS News Filter

RSS parser built with Python with a flexible trigger system to customize news stories the user sees on feed.

What It Does

This program fetches stories from live RSS news feeds (like Google News and Yahoo News), then filters them using a set of custom triggers I define. Only stories matching those triggers are shown in the final feed.

How It Works:

1. Fetching the News
   
Uses feedparser to grab articles from RSS feeds.

Parses each entry into a NewsStory object, which holds:

  GUID (unique ID)
  
  Title
  
  Description
  
  Link
  
  Publication date

2. Trigger System
   
A bunch of classes inherit from Trigger, each deciding whether a story is interesting based on different criteria.

Word Triggers:

  PhraseTrigger: fires when an exact phrase is found.
  
    TitleTrigger: fires when a word appears in the title.
    
    DescriptionTrigger: fires when a word appears in the description.
    
Time Triggers:

  BeforeTrigger / AfterTrigger: check publication date.

Composite Triggers:

  NotTrigger: negates another trigger.
  
  AndTrigger: fires if both triggers fire.
  
  OrTrigger: fires if either trigger fires.

3. User-defined Triggers
   
Triggers are set using a triggers.txt file, where I define my personal preferences in plain text. The file gets parsed to build a custom combo of triggers to filter the news feed.

4. GUI
   
Uses tkinter to display stories in a neat little window. You can scroll through headlines and read the juicy stories that passed your personal filter test.

Files:

  rssfeedparser.py: Handles the RSS fetching and story object creation.
  
  triggers.py: Contains all trigger class definitions.
  
  pset5.py: Main script that runs the whole system.
  
  triggers.txt: Your news filtering manifesto.

Requirements:

  Python 3
  
  feedparser
  
  tkinter (comes with most Python installs)

Install feedparser if needed:
'''
  pip install feedparser
'''
  
