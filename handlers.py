#!/usr/bin/env python


class load():
    def __init__(self, event):
        '''
        This is where all the handlers are importet and run on upstart.
        '''
        # keep in alphabetical order
        from cmdhandler import (
            headsup,
            help,
            shrug,
            slap,
            topic
        )

        headsup.headsup(event)
        help.help(event)
        shrug.shrug(event)
        slap.slap(event)
        topic.topic(event)
