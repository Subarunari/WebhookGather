# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.options import options
from logbook import RotatingFileHandler, info

from . import handler
from . import applicationconfig


options.define('proxy', type=bool, default=False, help="if proxy environment, indicate this option.")


def get_application():
    return tornado.web.Application([
        (r"/(?P<service>.+)", handler.Proxy, dict(needProxy=options.proxy)),
    ])


def log_setup():
    log = RotatingFileHandler(applicationconfig.LOG_PATH, max_size=104857600, backup_count=5)
    log.push_application()


def start():
    tornado.options.parse_command_line()

    application = get_application()
    application.listen(applicationconfig.PORT)
    log_setup()
    tornado.ioloop.IOLoop.current().start()
    info("Proxy run on port:{0}", applicationconfig.PORT)
