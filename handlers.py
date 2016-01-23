#!/usr/bin/env python


class load():
    def __init__(self, bot, handler_list):
        '''
        This is where all the handlers are imported and initialized on upstart
        '''

        cmdmodule = __import__("cmdhandler", fromlist=handler_list)
        for handler in handler_list:
            try:
                handler_module = getattr(cmdmodule, handler)
                handler_class = getattr(handler_module, handler)

                bot.handlers[handler] = handler_class(bot)
            except AttributeError:
                print("WARNING  Failed to load handler %s" % handler)
