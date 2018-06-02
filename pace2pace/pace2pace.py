#!/usr/bin/env python
import requests
import json
import pgpy
import sys
import re

from pace2pace_exceptions import Pace2PaceCouldNotLoadDocException, Pace2PaceDocSigInvalid, Pace2PaceUrlNotListedInDoc

class Pace2PaceActions:
    @staticmethod
    def eprint(args):
        sys.stderr.write(args)

    @staticmethod
    def testdoc(*params):
        help_text = '''Usage: pace2pace.py testdoc --url=<doc url> [--url=<additional url> ...]
'''
        urls = []
        next = None
        for param in params:
            if next == None:
                if param in ('-u', '--url'):
                    next = 'url'
                else:
                    Pace2PaceActions.eprint('Unknown param %s\n' % param)
                    Pace2PaceActions.eprint(help_text)
                    sys.exit(-1)
            elif next == 'url':
                urls += [param]
            else:
                Pace2PaceActions.eprint('Unknown param %s\n' % param)
                Pace2PaceActions.eprint(help_text)
                sys.exit(-1)

        if len(urls) == 0:
            Pace2PaceActions.eprint('Error, at least one url must be provided\n')
            Pace2PaceActions.eprint(help_text)
            sys.exit(-1)

        doc = Doc(urls)
        doc.load()
        doc.validate()
        print doc

class Doc:
    docText = None
    jsonText = None
    signature = None
    messageObject = None
    isVerified = False
    checkedUrl = None

    def __init__(self, urls, assumeValid=False):
        self.urls = urls
        self.assumeValid = assumeValid

    def parseDoc(self):
        self.pgpMessage = pgpy.PGPMessage()
        self.pgpMessage.parse(re.compile('\r\n').sub('\n',self.urlRes.text.encode('UTF8')))

    def parseJsonMessage(self):
        self.messageObject = json.loads(self.pgpMessage.message)

    def getAllowedUrls(self):
        return self.messageObject['urls']

    def getKey(self, key):
        pgp_key = pgpy.PGPKey()
        pgp_key.parse(self.messageObject['keys'][key]['key'])
        return pgp_key

    def load(self):
        self.urlRes = self.get_doc_from_urls();
        self.parseDoc()
        self.parseJsonMessage()

    def validate(self):
        # check if url in urls list
        if self.checkedUrl not in self.getAllowedUrls():
            raise Pace2PaceUrlNotListedInDoc(self.checkedUrl)

        rootKey = self.getKey('_ROOT')
        verifier = rootKey.verify(self.pgpMessage)
        if (not verifier):
            raise Pace2PaceDocSigInvalid(self.checkedUrl)
        self.isVerified = True

    def get_doc_from_urls(self):
        for url in self.urls:
            try:
                self.checkedUrl = url
                return requests.get(url)
            except:
                pass
        else:
            raise Pace2PaceCouldNotLoadDocException(self.urls)

    def __str__(self):
        return 'Pace2PaceDoc(urls={}, valid={})'.format(self.urls, self.isVerified)
    def __bool__(self):
        return self.isVerified

if __name__ == '__main__':
    action = None
    if len(sys.argv) > 1:
        action = sys.argv[1]

    if action in ('testdoc',):
        Pace2PaceActions.testdoc(*sys.argv[2:])
    else:
        Pace2PaceActions.eprint('''
Usage: pace2pace.py <action> [action params]

Actions: testdoc - checks url for doc validity
''')
        sys.exit(-1)
