# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from logbook import info, error

from .webhookconfig import WebhookConfig
from .webhookconfig import SectionNotFoundError
from .webhookconfig import UrlNotDefineError
from . import proxyconfig 


class Proxy(tornado.web.RequestHandler):
    def initialize(self, needProxy):
        self.needProxy = needProxy
        if not self.request.body:
            self.request.body = b'{}'

    @gen.coroutine
    def post(self, service):
        info("client_ip:{0},section:{1}", self.request.headers.get("X-Real-IP") or self.request.remote_ip, service)
        try:
            payload = tornado.escape.json_decode(self.request.body)
        except ValueError as e:
            self.set_status(400)
            self.write("Invalid JSON")
            error("BadRequest:{0}", e)
            self.finish()
            return

        try:
            webhook = WebhookConfig(service, payload)
        except SectionNotFoundError as e:
            self.set_status(500)
            self.write("SectionNotFound")
            error("Internal Server Error:{0}", e)
            self.finish()
            return
        except UrlNotDefineError as e:
            self.set_status(500)
            self.write("UrlNotDefine")
            error("Internal Server Error:{0}", e)
            self.finish()
            return

        tornado.options.parse_command_line()
        tornado.httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
        async_client = AsyncHTTPClient()
        req = tornado.httpclient.HTTPRequest(
            url=webhook.url,
            method="POST",
            body=tornado.escape.json_encode(webhook.payload),
            headers=tornado.httputil.HTTPHeaders({"content-type": "application/json charset=utf-8"}),
            proxy_host=proxyconfig.HOST if self.needProxy is True else None,
            proxy_port=proxyconfig.PORT if self.needProxy is True else None,
            follow_redirects=False,
            allow_nonstandard_methods=True
        )
        response = yield gen.Task(async_client.fetch, req)
        self.write(response.body)
        self.finish()
