class shrug:
    def __init__(self, bot):
        bot.add_event_handler("shrug", self.muc_shrug)
        self.bot = bot
        bot.register_help('shrug',
            'shows that you don\'t give a damn',
            'usage: !shrug <message>')

    def muc_shrug(self, msg):
        msg = msg[1]

        say = ""
        if msg['body'] != '':
            say = "\n      /" + u'\u00AF' + "- %s\n" % msg['body']

        emoji = u'\u00AF' + '\\_' + u'\u0028' + u'\u30C4' + u'\u0029' + '_/' + u'\u00AF'

        self.bot.send_message(mto=msg['from'].bare,
            mbody="%s%s" % (say, emoji),
            mtype='groupchat')
