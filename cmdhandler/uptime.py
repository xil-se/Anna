from datetime import datetime


class uptime:
    def __init__(self, bot):
        bot.add_event_handler("uptime", self.muc_uptime)
        self.bot = bot
        self.startTime = datetime.now()
        bot.register_help('uptime',
            'show server and bot uptime',
            'usage: !uptime')

    def muc_uptime(self, msg):
        from datetime import timedelta
        from utils import utils

        msg = msg[1]

        nowTime = datetime.now()
        botTime = nowTime - self.startTime

        with open('/proc/uptime', 'r') as f:
            upSeconds = float(f.readline().split()[0])
            serverTime = timedelta(seconds=upSeconds)

        serverTime = utils.delta_string(serverTime)
        botTime = utils.delta_string(botTime)

        body = 'Uptime: bot - %s, server - %s' % (botTime, serverTime)

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
