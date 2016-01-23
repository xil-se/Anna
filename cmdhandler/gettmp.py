import sqlite3


class gettmp:
    def __init__(self, bot):
        bot.add_event_handler("gettmp", self.muc_get_template)

        self.bot = bot
        bot.register_help('gettmp',
            'outputs the current template',
            'usage: !gettmp')

    def muc_get_template(self, msg):
        msg = msg[1]
        jid = msg['from'].bare
        db = sqlite3.connect('db.sq3')
        c = db.execute('SELECT template from topic where room_name = ?', [jid])
        self.bot.send_message(mto=jid,
            mbody=c.fetchone(),
            mtype='groupchat')
        db.close()
