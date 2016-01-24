import sqlite3


class topic:
    def __init__(self, bot):
        self.old_topic = {}
        '''
        register the event for "topic" and make the "event" available in self.bot.
        '''
        bot.add_event_handler("topic", self.muc_topic)
        bot.add_event_handler("groupchat_subject", self.set_old_topic)

        bot.schedule("Topic Fetch", 3600, self.update_topics, repeat=True)

        self.bot = bot
        bot.register_help('topic',
            'updates the topic from a template',
            'usage: !topic')
        bot.register_help('gettmp',
            'outputs the current template',
            'usage: !gettmp')

        self.update_topics()

    def set_old_topic(self, msg):
        jid = msg['from'].bare
        self.old_topic[jid] = msg["subject"]

        self.update_topics()

    def update_topics(self):
        db = sqlite3.connect('db.sq3')
        for row in db.execute('SELECT room_name, template FROM topic'):
            to = self.render_template(row[1])
            self.change_topic(row[0], to)

        db.close()

    def unix_time(self):
        import time
        return time.time()

    def isuphash(self, url):
        try:
            import requests
            import re
            import hashlib

            TAG_RE = re.compile(r'<[^>]+>')

            resp = requests.get(url)
            print("Url: %s has status: %s" % (url, resp.status_code))

            if resp.status_code < 400:
                return hashlib.md5(TAG_RE.sub('', resp.text).encode('utf-8')).hexdigest()

        except:
            print("sad panda request: %s" % url)

        return "false"

    def isup(self, url):
        try:
            import requests
            resp = requests.head(url)
            print("Url: %s has status: %s" % (url, resp.status_code))
            if resp.status_code < 400:
                return "Yes!"
        except:
            print("sad panda request: %s" % url)

        return "No."

    def days_until(self, date):
        from datetime import datetime
        from utils import utils

        try:
            as_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            delta = as_datetime - datetime.now()

            if delta.days < 0:
                return "the past"

            if delta.days == 0:
                return utils.delta_string(delta, show_seconds=False)
            else:
                return "%d days" % delta.days
        except e:
            return "dunno"

    def jsondecode(self, url):
        try:
            import json
            import requests
            resp = requests.get(url)
            if resp.status_code == 200:
                return json.loads(resp.text)

        except:
            print("sad panda request: %s" % url)

        return {}

    def render_template(self, t):

        from jinja2 import Template
        try:
            template = Template(t)
            template.globals.update(isup=self.isup)
            template.globals.update(isuphash=self.isuphash)
            template.globals.update(days_until=self.days_until)
            template.globals.update(unixtime=self.unix_time)
            template.globals.update(jsondecode=self.jsondecode)

            return template.render()
        except:
            return "Jinja failed"

    def change_topic(self, jid, topic):
        if jid in self.old_topic:
            if topic == self.old_topic[jid]:
                return

        self.old_topic[jid] = topic

        '''
        functiont to change a muc's topic
        '''
        msg = self.bot.make_message(jid)
        msg['type'] = 'groupchat'
        msg['subject'] = topic
        msg.send()

    def muc_topic(self, msg):
        self.update_topics()
