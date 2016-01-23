class headsup:
    def __init__(self, event):
        '''
        register the command and help message.
        '''
        event.add_event_handler("headsup", self.muc_headsup)
        self.event = event
        event.register_help('headsup',
            'highlights all users in the room',
            'usage: !headsup Your message')

    def muc_headsup(self, msg):
        '''
        Takes a message object as input and will generate
        a response that includes all the nicknames in the MUC.
        '''
        cmd = msg[0]
        msg = msg[1]
        self.nick = self.event.config['rooms'][msg['from'].bare]['nick']
        users = ''
        for i in self.event.plugin['xep_0045'].getRoster(msg['from'].bare):
            if i != (self.nick or msg['mucknick']):
                users = users + i + ', '

        self.event.send_message(mto=msg['from'].bare,
            mbody="%s See above!" % users,
            mtype='groupchat')
