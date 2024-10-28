from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
import json


class CustomKeyValueParser(BaseParser):
    media_type = 'text/plain'
    
    def parse(self, stream, media_type=None, parser_context=None):
        data = {}
        try:
            lines = stream.read().decode('utf-8').strip().splitlines()
            for line in lines:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        except Exception as e:
            raise ParseError("Could not parse data: {}".format(e))
    
        return data, media_type
    
class CustomJsonParser(BaseParser):
    media_type = 'application/json'
    format = 'json'
    def parse(self, stream, media_type=None, parser_context=None):
        try:
            data = json.loads(stream.read().decode('utf-8').strip())
            
            if isinstance(data, dict):
                data['parsed_by'] = 'CustomJsonParser'

            return data
        except Exception as e:
            raise ParseError("Could not parse data: {}".format(e))
