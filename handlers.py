#!/usr/bin/env python


class load():
    def __init__(self, bot):
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

        headsup.headsup(bot)
        help.help(bot)
        shrug.shrug(bot)
        slap.slap(bot)
        topic.topic(bot)
