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
        import urllib.request
        import urllib.parse

        url = "http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=%s" % urllib.parse.quote_plus(q)
        data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(data)

        if len(output["data"]) > 0:
            return output["data"]["image_original_url"];

        return "https://media.giphy.com/media/4SD55a1RnZCdq/giphy.gif"

    def muc_giphy(self, msg):
        msg = msg[1]

        body = self.giphy(msg['body'])

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
