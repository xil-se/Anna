class help:
    def __init__(self, event):
        '''
        register the event for "help" and make the "event" available in self.event.
        '''
        event.add_event_handler("help", self.muc_help, threaded=True)
        self.event = event
        event.register_help('help',
            'shows the help message',
            'usage: !help command')

    def muc_help(self, msg):
        '''
        Takes message object as input.
        Function to output the apropriate help.
        '''
        msg = msg[1]  # redefine message to lose the command
        enable_handlers = self.event.config['rooms'][msg['from'].bare]['enabled-handlers']
        try:
            if not msg['body'] == '':
                help = self.event.help[msg['body']]
                # check if no command for help was supplied and output general help
                if msg['body'] in enable_handlers or msg['body'] == 'help':
                    self.event.send_message(mto=msg['from'].bare,
                        mbody="\n%s:\n %s \n     %s" % (msg['body'], help[0], help[1]),
                        mtype='groupchat')
            else:  # output help for the command asked for
                ans = '\nCommands: \n'
                for i in self.event.help:
                    if i in enable_handlers or i == 'help':
                        ans = "%s    %s - %s\n" % (ans, i, self.event.help[i][0])

                self.event.send_message(mto=msg['from'].bare,
                    mbody=ans[:-1],
                    mtype='groupchat')
        except:
            pass
