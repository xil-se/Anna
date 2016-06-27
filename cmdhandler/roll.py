class roll:
    def __init__(self, bot):
        '''
        Register the command and the help.
        Also seed some randomness.
        '''

        bot.add_event_handler("roll", self.muc_roll)
        self.bot = bot
        bot.register_help('roll',
            'rolls dice',
            'usage: !roll NdS (N - how many times, S - how many sides)')

    def roll(self, i, d):
        from random import randint

        sum = 0
        for x in range(0, i):
            sum = sum + randint(1, d)

        return sum

    def muc_roll(self, msg):
        import re

        msg = msg[1]

        match = re.search("([0-9]*)d([0-9]+)", msg['body'])
        if match:
            try:
               i = int(match.group(1) if match.group(1) is not None else 1)
            except:
                i = 1

            try:
                d = int(match.group(2))
            except:
                d = 6

            body = "Rolled %dd%d: %d" % (i, d, self.roll(i, d))
        else:
            body = "This is serious business, %s..." % msg['mucnick']

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
