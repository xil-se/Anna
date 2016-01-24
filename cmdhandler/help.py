class help:
    def __init__(self, bot):
        '''
        register the event for "help" and make the "event" available in self.bot.
        '''
        bot.add_event_handler("help", self.muc_help, threaded=True)
        self.bot = bot
        bot.register_help('help',
            'shows the help message',
            'usage: !help command')

    def muc_help(self, msg):
        '''
        Takes message object as input.
        Function to output the apropriate help.
        '''
        msg = msg[1]  # redefine message to lose the command
        body = ''
        # no exception below because help would not work if enabled-handlers was undefined
        enable_handlers = self.bot.config['rooms'][msg['from'].bare]['enabled-handlers']
        if not msg['body'] == '':
            # output help for the requested command
            if msg['body'] in enable_handlers:
                help = self.bot.help[msg['body']]
                body = "\n%s:\n %s \n     %s" % (msg['body'], help[0], help[1])
            else:
                body = "Command not found"
        else:
            # output general help
            body = "\nTo get details about a specific command, use !help <command>\n"
            body = body + "Commands: \n"
            for i in sorted(self.bot.help):
                if i in enable_handlers:
                    body = "%s    %s - %s\n" % (body, i, self.bot.help[i][0])

            body = body[:-1]

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
