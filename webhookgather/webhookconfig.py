# -*- coding: utf-8 -*-

import configparser


class WebhookConfig:
    INI_PATH = "webhook.ini"

    def __init__(self, section, payload):
        """
            return: incoming webhook url&params based on section
        """
        config = self._read_config_file()
        self.payload = payload

        if config.has_section(section):
            self.url = config.get(section, "url", fallback=None)
            if self.url is None:
                raise UrlNotDefineError()

            setting_payload_keyset = set(config.options(section))
            request_payload_keyset = set(payload)
            keys = ()
            keys = setting_payload_keyset.difference(request_payload_keyset)

            for key in keys:
                self.payload[key] = config.get(section, key)

        else:
            raise SectionNotFoundError(section)

    def _read_config_file(self):
        config = configparser.SafeConfigParser()
        config.read(self.INI_PATH)
        return config


class SectionNotFoundError(Exception):
    def __init__(self, section):
        self.message = section + " is not defined in the Webhook.ini."

    def __str__(self):
        return repr(self.message)


class UrlNotDefineError(Exception):
    def __init__(self):
        self.message = "url is not defined in the Webhook.ini."

    def __str__(self):
        return repr(self.message)
