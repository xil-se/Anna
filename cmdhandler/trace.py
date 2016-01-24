class trace:
    def __init__(self, bot):
        bot.add_event_handler("trace", self.muc_trace)
        self.bot = bot
        bot.register_help('trace',
            'traces a host',
            'usage: !trace host_to_trace')

    def trace(self, host):
        import subprocess

        args = ['mtr', host, '--report-wide', '-c', '1']
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.decode("UTF-8")

        lines = out.split('\n')
        if len(lines) > 11:
            return '\n'.join(lines[:10] + ['--snip--'] + lines[-2:-1])

        return out

    def muc_trace(self, msg):
        msg = msg[1]
        host = msg['body'].strip()

        if host == '':
            body = "Please specify a host, see !help trace"
        else:
            body = ''.join(["Tracing ", host, '\n', self.trace(host)])

        self.bot.send_message(mto=msg['from'].bare,
            mbody=body,
            mtype='groupchat')
