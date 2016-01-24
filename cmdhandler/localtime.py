class localtime:
    def __init__(self, bot):
        bot.add_event_handler("localtime", self.muc_localtime)
        self.bot = bot
        bot.register_help('localtime',
            'shows local time',
            'usage: !localtime')

    def muc_localtime(self, msg):
        from datetime import datetime
        from dateutil import tz

        msg = msg[1]

        localTime = datetime.now(tz.tzlocal())
        body = "Local time: %s" % localTime.strftime('%Y-%m-%d %H:%M:%S')

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
