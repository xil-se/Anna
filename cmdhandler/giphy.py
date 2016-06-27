class giphy:
    def __init__(self, bot):
        bot.add_event_handler("giphy", self.muc_giphy)
        self.bot = bot
        bot.register_help('giphy',
            'returns a random GIF',
            'usage: !giphy phrase')

    def giphy(self, q):
        import json
        import urllib
        import urllib2

        data = json.load(urllib2.urlopen("http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=%s" % urllib.quote_plus(q)))

        if len(data["data"]) > 0:
            return data["data"]["image_original_url"];

        return "https://media.giphy.com/media/4SD55a1RnZCdq/giphy.gif"

    def muc_giphy(self, msg):
        msg = msg[1]

        body = self.giphy(msg['body'])

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
