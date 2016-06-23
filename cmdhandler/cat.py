class cat:
    def __init__(self, bot):
        bot.add_event_handler("cat", self.muc_cat)
        self.bot = bot
        bot.register_help('cat',
            'cats!!',
            'usage: !cat')

    def muc_cat(self, msg):
        msg = msg[1]
        try:
            apikey = self.bot.config['catapi']['api_key']
            import requests
            r = requests.get('http://thecatapi.com/api/images/get?format=src&api_key=%s' %(apikey),
                allow_redirects=False)
            say = r.headers['Location']
        except Exception as e:
            say = e

        self.bot.send_message(mto=msg['from'].bare,
            mbody="%s" % (say),
            mtype='groupchat')
