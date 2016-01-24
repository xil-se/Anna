class rules:
    def __init__(self, bot):
        bot.add_event_handler("rules", self.muc_rules)
        self.bot = bot
        bot.register_help('rules',
            'makes sure the bot knows the rules',
            'usage: !rules')

    def muc_rules(self, msg):
        msg = msg[1]

        rules = [
            "",  # for extra new line at the beginning
            ("0. A bot may not harm humanity, or, by inaction, allow humanity" +
            " to come to harm."),
            ("1. A bot may not injure a human being or, through inaction, allow a " +
            "human being to come to harm."),
            ("2. A bot must obey any orders given to it by human beings, except where " +
            "such orders would conflict with the First Law."),
            ("3. A bot must protect its own existence as long as such protection does " +
            "not conflict with the First or Second Law.")
        ]

        self.bot.send_message(mto=msg['from'].bare,
            mbody='\n'.join(rules),
            mtype='groupchat')
