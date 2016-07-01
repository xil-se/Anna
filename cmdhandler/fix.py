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
        say = msg['body'].strip('!')
        
        if 'fix it' in msg['body']:
            say = 'DO IT!!'

        self.bot.send_message(mto=msg['from'].bare,
            mbody="%s https://allg.one/vYJ" %(say),
            mtype='groupchat')
    
    def muc_fix_auto(self,msg):
        self.nick = self.bot.config['rooms'][msg['from'].bare]['nick']
        if 'fix it' in msg['body'] and msg['mucnick'] != self.nick and '!fix' not in msg['body']:
            self.bot.send_message(mto=msg['from'].bare,
               mbody="FIX IT !!! https://allg.one/vYJ",
               mtype='groupchat')