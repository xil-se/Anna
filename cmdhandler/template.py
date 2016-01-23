import sqlite3


class template:
    def __init__(self, bot):
        bot.add_event_handler("template", self.muc_update_template)

        self.bot = bot
        bot.register_help('template',
            'sets topic template',
            'usage: !template <template>')

    def muc_update_template(self, msg):
        '''
        This function will change the topic of the muc uppon bot.
        '''
        msg = msg[1]
        jid = msg['from'].bare

        db = sqlite3.connect('db.sq3')
        db.execute('REPLACE INTO topic (room_name, template) VALUES (?,?)',
            (jid, msg['body']))
        db.commit()
        db.close()

        self.bot.handlers['topic'].update_topics()
