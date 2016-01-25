import tornado.testing
import tornado.web

from . import server

BROKEN_JSON = b'{"a"}'
UNKNOWN_SECTION = "/d62faf7883be431b829627df064af944"


class TestApp(tornado.testing.AsyncHTTPTestCase):
    # test target is run
    def get_app(self):
        return server.get_application()
    
    # test
    def test_unknown_section(self):
        response = self.fetch(UNKNOWN_SECTION, method="POST", body=b'{}')
        self.assertEqual(response.code, 404)
        self.assertEqual(response.body, b"NotFound")
        
    def test_broken_json(self):
        response = self.fetch('/sandbox', method="POST", body=BROKEN_JSON)
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b"BadRequest")
