class slap:
    def __init__(self,event):
        '''
        Register the command and the help.
        Also seed some randomness.
        '''
        import random
        event.add_event_handler("slap",self.muc_slap)
        self.event = event
        event.register_help('slap','slaps a user in the room','usage: !slap user')

    def randnumber(self,mn):
        '''
        Simple generator that will return a random int.
        '''
        random=self.event.random
        while True:
            yield random.randint(0,mn)

    def muc_slap(self,msg):
        '''
        Takes message object as input.
        It will respond to the message with a random slap.
        '''
        cmd=msg[0]
        msg=msg[1]
        self.nick= self.event.config['rooms'][msg['from'].bare]['nick']
        slaps=[
                ' large trout',
                ' slimy toad',
                ' small car',
                'n angry weasel',
                ' problematic customer',
                'n overpriced iPad',
                ' pile of overpriced Windows licenses',
                'n overheated Xbox 360'
        ]

        if ('Simon' in msg['body'] or 'david' in msg['body']) or (self.nick in msg['body'] and 'Simon' not in msg['mucnick']):
            victim=msg['mucnick']
        elif(msg['mucnick'] == 'Troels'):
            victim=msg['mucnick']
        else:
            victim=msg['body']
        c=next(self.randnumber(len(slaps)-1))
        self.event.send_message(mto=msg['from'].bare,
            mbody="/me slaps %s with a%s!" %(victim,slaps[c]),
            mtype='groupchat')
