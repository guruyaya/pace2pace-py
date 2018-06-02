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

        docReader = DocReader(urls)
        docReader.load()
        docReader.validate()
        print docReader

class DocReader:
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
        self.urlRes = self.getDocFromUrls();
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

    def getDocFromUrls(self):
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

class RequestProceesor:
    ''' This class gets a request and handles it'''
    request = None
    isValid = False
    doc = None
    validationKeyName = None
    validationKey = None

    def __init__(self, requestJson):
        self.requestJson = requestJson

    def load(self):
        # parse the reuqest json
        self.request = json.loads(requestJson)
        # load the attached doc
        self.doc = DocReader(self.request['urls'])
        self.doc.load()
        self.doc.validate()
        # get the validation key


    def validate(self):
        # laod key
        # validate against requested key
        pass

class BaseLoginValidation:
    ''' This class handles the process of validating login process
note that this is the basic implemetation. The specific implementation of the protocol, must be applied as extention of this class
    '''
    def __init__(self, privateKey, encodedRequest):
        self.privateKey = privateKey
        self.encodedRequest = encodedRequest
        self.validationString = validationString

    def load(self):
        # decode the endcoded request
        # validate string
        # load / validate doc
        # validate request
        pass

    def getValidationString(self):
        '''
        '''
        pass

    def validate(self):
        pass

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
