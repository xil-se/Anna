#!/usr/bin/env python

class load():
    def __init__(self,event):
        '''
        This is where all the handlers are importet and run on upstart.
        '''
        from cmdhandler import headsup,slap,topic,help

        headsup.headsup(event)
        slap.slap(event)
        topic.topic(event)
        help.help(event)
