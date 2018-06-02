
class Pace2PaceException(Exception):
    pass

class Pace2PaceCouldNotLoadDocException(Pace2PaceException):
    def __init__(self, urls):
        Exception.__init__(self, 'Could not load any of the urls: %s' % urls)

class Pace2PaceDocSigInvalid(Pace2PaceException):
    def __init__(self, url):
        Exception.__init__(self, 'PGP Signature of %s not valid' % url)

class Pace2PaceUrlNotListedInDoc(Pace2PaceException):
    def __init__(self, url):
        Exception.__init__(self, 'Url %s not listed in doc' % url)
