from flask import request
import logging


class RequestFormatter(logging.Formatter):

    def format(self, record):
        # you can set here everything what you need
        # I just added url and id from GET parameter
        record.id = request.args.get('id')
        record.url = request.url
        return super().format(record)