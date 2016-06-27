class isup:
    def __init__(self, bot):
        bot.add_event_handler("isup", self.muc_isup)
        self.bot = bot
        bot.register_help('isup',
            'checks if a host/ip is up',
            'usage: !isup host/ip')

    def giphy(self, q):
        import json
        import urllib
        import urllib2

        data = json.load(urllib2.urlopen("http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=%s" % urllib.quote_plus(q)))

        if len(data["data"]) > 0:
            return data["data"]["image_original_url"];

        return "https://media.giphy.com/media/4SD55a1RnZCdq/giphy.gif"

    def muc_isup(self, msg):
        import urllib2

        msg = msg[1]
        url = msg['body'].strip()
        body = ""

        if len(url) == 0:
            body = "Stop screwing around!"
        else:
            resp = urllib2.urlopen("http://isup.me/%s" % url).read()
            if "Huh?" in resp:
                body = "How about a valid URL next time?"
            else:
                body = "%s seems to be %s!" % (url, "down" if "looks down" in resp else "up")

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
