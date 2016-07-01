class fix:
    def __init__(self, bot):
        bot.add_event_handler("fix", self.muc_fix)
        bot.add_event_handler("groupchat_message", self.muc_fix_auto)
        self.bot = bot
        bot.register_help('fix',
            'FIX IT!!',
            'usage: !fix')

    def muc_fix(self, msg):
        msg = msg[1]

        self.bot.send_message(mto=msg['from'].bare,
            mbody="%s https://allg.one/vYJ" %(msg['body']),
            mtype='groupchat')
    
    def muc_fix_auto(self,msg):
        if 'fix it' in msg['body']:
            self.bot.send_message(mto=msg['from'].bare,
               mbody="FIX IT !!! https://allg.one/vYJ",
               mtype='groupchat')