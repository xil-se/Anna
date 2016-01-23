class slap:
    def __init__(self, bot):
        '''
        Register the command and the help.
        Also seed some randomness.
        '''
        import random
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
        slaps = [
            ' large trout',
            ' slimy toad',
            ' small car',
            'n angry weasel',
            ' problematic customer',
            'n overpriced iPad',
            ' pile of overpriced Windows licenses',
            'n overheated Xbox 360'
        ]

        is_simon = 'Simon' in msg['body']
        is_david = 'david' in msg['body']
        is_self = self.nick in msg['body']
        if (is_simon or is_david) or (is_self and not is_simon):
            victim = msg['mucnick']
        else:
            victim = msg['body']

        c = next(self.randnumber(len(slaps) - 1))
        self.bot.send_message(mto=msg['from'].bare,
            mbody="/me slaps %s with a%s!" % (victim, slaps[c]),
            mtype='groupchat')
