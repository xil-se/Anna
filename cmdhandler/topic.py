import sqlite3


class topic:
    def __init__(self, event):
        #self.template_topic = {}
        self.old_topic = {}
        '''
        register the event for "topic" and make the "event" availeble in self.event.
        '''
        event.add_event_handler("topic", self.muc_topic)
        event.add_event_handler("template", self.muc_update_template)
        event.add_event_handler("gettmp", self.muc_get_template)
        event.add_event_handler("groupchat_subject", self.set_old_topic)

        event.schedule("Topic Fetch", 3600, self.update_topics, repeat=True)

        self.event = event
        event.register_help('topic',
            'Updates the topic from a template',
            'usage: !topic')
        event.register_help('template',
            'Sets topic template',
            'usage: !template <template>')
        event.register_help('gettmp',
            'Outputs the current template',
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
            #import httplib
            #from urlparse import urlparse
            #p = urlparse(url)

            #conn = httplib.HTTPConnection(p.netloc, timeout=1)
            #conn.request('HEAD', p.path)
            #resp = conn.getresponse()
            import requests
            resp = requests.head(url)
            print("Url: %s has status: %s" % (url, resp.status_code))
            if resp.status_code < 400:
                return "Yes!"
        except:
            print("sad panda request: %s" % url)

        return "No."

#    def days_until(self, date):
#        from datetime import datetime
#
#        try:
#            d1 = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
#            days = int((round((d1 - datetime.now() ).days, 0)))
#            if days <= 0:
#                return 0
#
#            return days
#        except:
#            return "0"

    def days_until(self, date):
        from datetime import datetime

        try:
            d1 = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            dt = (d1 - datetime.now())

            if dt.days < 0:
                return "Nononono"

            if dt.days == 0:
                h = divmod(dt.seconds, 3600)
                m = divmod(h[1], 60)
                return "%d days, %d hours, %d minutes" % (dt.days, h[0], m[0])
            else:
                return "%d days" % dt.days
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
        msg = self.event.make_message(jid)
        msg['type'] = 'groupchat'
        msg['subject'] = topic
        msg.send()

    def muc_get_template(self, msg):
        msg = msg[1]
        jid = msg['from'].bare
        db = sqlite3.connect('db.sq3')
        c = db.execute('SELECT template from topic where room_name = ?', [jid])
        self.event.send_message(mto=jid,
            mbody=c.fetchone(),
            mtype='groupchat')
        db.close()

    def muc_update_template(self, msg):
        '''
        This function will change the topic of the muc uppon event.
        '''
        msg = msg[1]
        jid = msg['from'].bare
        #self.template_topic[jid] = msg['body']

        db = sqlite3.connect('db.sq3')
        db.execute('REPLACE INTO topic (room_name, template) VALUES (?,?)',
            (jid, msg['body']))
        db.commit()
        db.close()

        self.update_topics()

        #topic = self.render_template(self.template_topic[jid])

        #self.change_topic(jid,topic)

    def muc_topic(self, msg):
        self.update_topics()
