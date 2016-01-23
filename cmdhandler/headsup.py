class headsup:
    def __init__(self, bot):
        '''
        register the command and help message.
        '''
        bot.add_event_handler("headsup", self.muc_headsup)
        self.bot = bot
        bot.register_help('headsup',
            'highlights all users in the room',
            'usage: !headsup Your message')

    def muc_headsup(self, msg):
        '''
        Takes a message object as input and will generate
        a response that includes all the nicknames in the MUC.
        '''
        cmd = msg[0]
        msg = msg[1]
        self.nick = self.bot.config['rooms'][msg['from'].bare]['nick']
        users = ''
        for i in self.bot.plugin['xep_0045'].getRoster(msg['from'].bare):
            if i != (self.nick or msg['mucknick']):
                users = users + i + ', '

        self.bot.send_message(mto=msg['from'].bare,
            mbody="%s See above!" % users,
            mtype='groupchat')
