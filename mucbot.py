#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import sys
import logging
import getpass
from optparse import OptionParser
import re
import sleekxmpp
import handlers
from configobj import ConfigObj
import random
from time import time
import requests
#utf8 all the things
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class MUCBot(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will greets those
    who enter the room, and acknowledge any messages
    that mentions the bot's nickname.
    """

    def __init__(self):
        self.config = ConfigObj('config.ini')
        jid = self.config['general']['jid']
        password = self.config['general']['password']
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        #self.room = room
        #self.nick = nick
        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        self.help = {}
        commands = handlers.load(self)
        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("groupchat_message", self.muc_message)
        #self.add_event_handler("groupchat_message", self.muc_slap)
        #self.add_event_handler("groupchat_message", self.muc_headsup)
        #self.add_event_handler("slap",self.muc_slap)

        self.add_event_handler("groupchat_message", self.muc_command)
        # The groupchat_presence event is triggered whenever a
        # presence stanza is received from any chat room, including
        # any presences you send yourself. To limit event handling
        # to a single room, use the events muc::room@server::presence,
        # muc::room@server::got_online, or muc::room@server::got_offline.
        #self.add_event_handler("muc::%s::got_online" % self.room,
        #                       self.muc_online)
        random.seed(time() + 4)
        self.random = random

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()

        for i in self.config['rooms']:
            password = self.config['rooms'][i].get('password', None)
            if(password is not None):
                self.plugin['xep_0045'].joinMUC(i,
                    self.config['rooms'][i]['nick'],
                    # If a room password is needed, use:
                    password=password,
                    wait=True)
            else:
                self.plugin['xep_0045'].joinMUC(i,
                    self.config['rooms'][i]['nick'],
                    # If a room password is needed, use:
                    #password=self.config['rooms'][i]['password'],
                    wait=True)

    def muc_command(self, msg):
        """
        This function will check for a command in the incoming message.
        It will then check if the command is valid in the room and if it is
        it will fire the commands event.
        """
        m = re.search('^\!([a-z0-9]*) (.*)', msg['body'], re.DOTALL | re.IGNORECASE)
        m2 = re.search('^\!(.*)$', msg['body'])
        enabled_handlers = self.config['rooms'][msg['from'].bare]['enabled-handlers']

        if m:
            msg['body'] = m.group(2)
            if (m.group(1) in enabled_handlers or m.group(1) in ['help']):
                self.event(m.group(1), [m.group(1), msg])
        elif m2:
            msg['body'] = ''
            if (m2.group(1) in enabled_handlers or m2.group(1) in ['help']):
                self.event(m2.group(1), [m2.group(1), msg])

    def register_help(self, cmd, shortmsg, msg):
        '''
        Register the help messages.
        '''
        self.help[cmd] = [shortmsg, msg]

    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        Whenever the bot's nickname is mentioned, respond to
        the message.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        This handler will reply to messages that mention
        the bot's nickname.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        replies = [
            "Don't mention the war.",
            "I'm not that into Pokemon",
            "I won't even comment on that.",
            "That sounds interesting. Tell me more.",
            "Did you know that mongoDB is webscale?",
            "I think there is an app for that.",
            "Did you know that the bird is greater than or equal to the Word?",
            "Is that some kind of javascript framework?",
            "Pics or it didn't happen!",
            "What if i told you that i am not a bo(a)t?"
        ]
        self.nick = self.config['rooms'][msg['from'].bare]['nick']
        if msg['mucnick']:
            if msg['mucnick'] == 'David' and self.nick in msg['body']:
                self.send_message(mto=msg['from'].bare,
                    mbody="Yes sir!",
                    mtype='groupchat')
            elif msg['mucnick'] != self.nick and self.nick in msg['body']:
                reply = replies[self.random.randint(1, len(replies)) - 1]
                self.send_message(mto=msg['from'].bare,
                    mbody="%s, %s" % (msg['mucnick'], reply),
                    mtype='groupchat')


if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet',
                    help='set logging to ERROR',
                    action='store_const',
                    dest='loglevel',
                    const=logging.ERROR,
                    default=logging.INFO)
    optp.add_option('-d', '--debug',
                    help='set logging to DEBUG',
                    action='store_const',
                    dest='loglevel',
                    const=logging.DEBUG,
                    default=logging.INFO)
    optp.add_option('-v', '--verbose',
                    help='set logging to COMM',
                    action='store_const',
                    dest='loglevel',
                    const=5,
                    default=logging.INFO)

    # JID and password options.
   #optp.add_option("-j", "--jid", dest="jid",
    #                help="JID to use")
    #optp.add_option("-p", "--password", dest="password",
     #               help="password to use")
   # optp.add_option("-r", "--room", dest="room",
    #                help="MUC room to join")
    #optp.add_option("-n", "--nick", dest="nick",
     #               help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    #if opts.jid is None:
     #   opts.jid = raw_input("Username: ")
    #if opts.password is None:
        #opts.password = getpass.getpass("Password: ")
    #if opts.room is None:
      #  opts.room = raw_input("MUC room: ")
    #if opts.nick is None:
     #   opts.nick = raw_input("MUC nickname: ")

    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MUCBot()
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp.register_plugin('xep_0060')  # pubsub

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
