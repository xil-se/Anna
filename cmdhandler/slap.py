class slap:
    def __init__(self, bot):
        '''
        Register the command and the help.
        Also seed some randomness.
        '''
        import random

        self.slaps = []
        with open('slaps.txt') as f:
            for line in f.readlines():
                self.slaps.append(line[:-1])  # strip new line

        bot.add_event_handler("slap", self.muc_slap)
        self.bot = bot
        bot.register_help('slap',
            'slaps a user in the room',
            'usage: !slap user')

    def randnumber(self, mn):
        '''
        Simple generator that will return a random int.
        '''
        random = self.bot.random
        while True:
            yield random.randint(0, mn)

    def muc_slap(self, msg):
        '''
        Takes message object as input.
        It will respond to the message with a random slap.
        '''
        cmd = msg[0]
        msg = msg[1]
        self.nick = self.bot.config['rooms'][msg['from'].bare]['nick']

        is_master = msg['body'].lower() in self.bot.masters
        is_self = self.nick in msg['body']
        if is_master or (is_self and not is_master):
            victim = msg['mucnick']
        elif msg['body'] == '':
            victim = "someone"
        else:
            victim = msg['body']

        c = next(self.randnumber(len(self.slaps) - 1))
        self.bot.send_message(mto=msg['from'].bare,
            mbody="/me slaps %s with %s!" % (victim, self.slaps[c]),
            mtype='groupchat')
