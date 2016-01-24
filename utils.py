class utils:
    @staticmethod
    def delta_string(delta, show_seconds=True):
        h = divmod(delta.seconds, 3600)
        m = divmod(h[1], 60)
        s = divmod(m[1], 60)

        t = []
        if delta.days > 0:
            t.append("%d day%s" % (delta.days, "" if delta.days == 1 else "s"))

        if h[0] > 0:
            t.append("%d hour%s" % (h[0], "" if h[0] == 1 else "s"))

        if m[0] > 0:
            t.append("%d minute%s" % (m[0], "" if m[0] == 1 else "s"))

        if s[1] > 0 and show_seconds:
            t.append("%d second%s" % (s[1], "" if s[0] == 1 else "s"))

        if len(t) == 0:
            t.append('ett ' + u'\u00F6' + 'gonblick')

        return ' '.join(t)
