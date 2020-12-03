import unittest
import tempfile
import os
import json
import logging

from pgpy.errors import PGPDecryptionError, PGPError

from pace2pace_client import Pace2PaceMasterRequest, NewUserRequest
from pace2pace_master import RootKey, RootKeyChain
# constants
TEST_PRV_KEY = '-----BEGIN PGP PRIVATE KEY BLOCK-----\n\n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\nO8+S5zMsa4oIxKHJcim3JD9NVV4=\n=H713\n-----END PGP PRIVATE KEY BLOCK-----\n'
TEST_PUB_KEY = '-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nxsFNBF+31/MBEADwuph4rqdHJlzpg0GjeE3ao94Zpuo6EDrU+fxaWKjzNYSZZw03\nXya19xPXSt64/1LybZfHP+JUeITtC0qcnl0WfLQJi9Y+Bgva3CzSDJbb/S2ZPYSa\nV1qLrKdhNr09zrN6jIYG4Fb1Y8f8fzyxjokSuKEM9wXC0NpRvJPQI0vGmpCm/maf\ncph+gx9nIJmdrxn1hY+/mL1PH7H8duSLLUvCZttxbCZS4+qoKX1PPhJpMcGPj063\np1dpGyGU91NSW6xvUUw3B0KyHYT3VXDZQtxEsVa7HzsKZzCUxxSTAWM8lurrG/rZ\nNcNxNPOUV/Vas2rmSYDL6aI40SPU6F8pRRUUwevBqxzzkaHol4ollIqTSXvCCAPG\nd9yjmvB4/mSax2IDNmhQrKymteanTDsVsbEWNwIB5XpBZr0Y2l8EvkWQF1aZY6+A\nULsLgvDtHlpkbbVZyqK6Kb+gn/kvz1LY9eJAOSOp3FmW5stGwbBCWUqSBkhcK1Sn\n/MELFhkNJy39cG0w2EP+MYzgoi2efQHeGytXngyA8oHyHPbC/RUOgbqxSlUFvVZr\ne6j92XKVAJsJIGmp5C1hcWFZxuZQ+LyAaUXcViwJcvhMIpmgrV3b8Iswl+2UpgUW\ne9PV+ZH/mB1SfKO1byyZ4h3LXWLJHkfp9c8yW5MZj9Cs4nM6NR4oYwPpOwARAQAB\nzQxQYWNlMlBhY2VrZXnCwYoEEwEIADQFAl+31/QCGw4ECwkIBwUVCAkKCwUWAgMB\nAAIeARYhBCS5JYo2FByhjPdnyvQkIfkK51vOAAoJEPQkIfkK51vOTycP/RvEIRL7\nXIaFeOD6G/P6JFsHeYlu7znDDb9WQpAfkQnRUFnhmHyGCyRGVvIQMH2sDEQDeBGD\nVU4w2Eq3zL9rg+tUnZTJoItjHHQMBFrFUOFPr6bloNE16zosFMCKlgZDybXfkw4z\nHiqIm9V6J4dkA2LSTtkvP8lAVZbOdSzxjQ7T7TlZmRYjdlhQMD4DGYy4dLUGvR/o\nCb7j8zK7C/vVgAJNL2GClrs9V1wmBfVpX3ruNnfWzP41/P/KBFPLJChNoDcIn7Y/\n03jlvD1Gyl9S2KUanTl41Lkktcuzu8/EsEwHMrsRguLE2eS2AqT6eBuroy/mBF4j\nhm/mmAMnTHYG8uTdKViIwmWJ50DM6cBPqVDJ8DuQK0AjzMJm40CGtxJMnYurF7Ws\nnBZoYI7T+np8w5ETb50G7BBm2bsibYIDUnNejHBmHoouqfljdMYH3WDX1aUYLz1F\n0MGcxbUewx+BRvfda+xdc9KrAj+jXQtkRX4+2lEu65c1P0mH6mfbGQ/LVCmp+Emb\n1XnazfGhylYycIIC92oL8STeAwNylftTS3siPeIMi2gAYW3SMi6p4elejuJvk7I3\nbCQfS+PNrzHgT/ekE22Sf7ICa74HXINnLEUTcPFXvxNqA/OfhdENnLhP9pEXb6aw\nBVpHX4sZWTvPkuczLGuKCMShyXIptyQ/TVVe\n=6SCa\n-----END PGP PUBLIC KEY BLOCK-----\n'
TEST_PRV_PASS = '1234'

INVALID_PRV_KEY = 'SOME STRING'
WRONG_PUB_KEY = '-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nxsFNBF+341wBEACc39VdIG1eFyMAvdNuGO4dVb+h6rIXn5kyoTkDPNTYksiYPK/K\nMe6fB9tv+apwD8SRDA9BWBFAbr4zXaKDksh4Ony1UlI89qaSmpYxWkttILI6nR1w\nNjmoIA3IPNJuJ/5j0PPPBuzFZWjxLmX/s/9zTJ72FXwFjKG88JOSBtm7ec5ni7Y7\ncGZoh3fhx5XbFK4iGwHLsRiekK1F0XVHSOuX53PoHmfeqnqQk0XPdUVuIL+nA+i7\n0XSniuJQo+4o7TYGTYPH0U3v1WZKbWttIzSNkQifpD18lI3u5jGDvowW1ylnxxGt\nfDNtshK9Udv5QlEm2ruz5ShduTVV9t5B/OL+oB5htCdmO9xldHo3pddsrbFeCBtp\nIuoYuAYZ+VD+hSNaZasc8mor8wbFSFyGOsc52ipS8iY7hID0MnnmZWdIuI9PanRl\nBJLrQyRXbxUq2btkUxsH7daZBlieXLdr98fkkxrAS3ah5PJQ5psRZQWZEpTcVc8j\n2RpUafPp8Bx29GCgI0fX3agVUtO0ps+1LXC9EYK8OeEf8zePUi4Y0geEoYczKOS8\n1zjD53fLo2RDqPh1SLQ+nI88IcMCN2jFUTbqC1CNkC1LXdmoUE7RRmcRviy+aGZJ\nAmNOqGEjvEfs2UbI2o/GOJZP4DVKURuOeZrqsrD0VVtxcltq8/hRY43mOwARAQAB\nzQxQYWNlMlBhY2VrZXnCwYoEEwEIADQFAl+341wCGw4ECwkIBwUVCAkKCwUWAgMB\nAAIeARYhBNb6hvbqopgNBhFJ1gCL3Dd46tUSAAoJEACL3Dd46tUSuGIQAJBuIboy\nrxH8BkCNIcOZsYx2BT+lMZDK1af4a1taWQ6nssD3c6l0rXD8wX82zJG+vUZElPfM\nzY1B+xnNM2AvxFmyGguMXUTYW1hC9GkhpHE7ObTNMGf1sOr4ejVz1QQGwbHGXoBT\nx/Hk9pNcVedotZPNeiTdbLtHa4/xdSiHdX0WbuhlJTo+CcbVIp5TwyskOHqXL0fT\nsZtGkqMczD9mq7P5nDxYoUZ7TZG/d5Qcj8B320CvXMFum/MF83H0EurRaDYjmXSA\nMCi797cMFQQQHvlwitmq/vDnOtHEmO7+UxizIoFOMkWSxjtTCl1fJ3HrJO0IE8ho\n7NQ5QhwMCtQQdCC+l1OzARas3fKqEQQsoa6GSucNYfpMrr0jDU3GWitKDyQUt/93\nwz2F+1OAJ08efQqXWYCx5cQI0NfXIQgO0cPG+vu11uX7LL0AhV7d3H9WsMSfCGSY\n4sGoahUsaNq3BHpc3of6+MDxqxSMpSFh2KO+s/bndnvNZG6oha1WjhGwt8+QBSGJ\nkAyyzgdw57MdPL6RuA+ddtkOuY8tdKb823id1qt4rtl7yibM3gb0C4tKH9Bj5LiI\noBJq9kSbfrZOO86PXjHKSlnVJ4XrNkcN72cZa3d/c8evfNeUpQaP9Se4aE8LAu2H\n06vfRt7Vtnyox53BGSkTVT0Bgius683TEHiF\n=VdPz\n-----END PGP PUBLIC KEY BLOCK-----\n'
class pace2pace_master_client_test(unittest.TestCase):
    def test_gen_request(self):
        genreq = Pace2PaceMasterRequest('this', {'is': 'a test'})
        self.assertEqual(genreq.action, 'this')
        self.assertEqual(genreq.data, {'is': 'a test'})
        self.assertEqual(genreq.version, 0.1)

        # errors
        with self.assertRaises(NotImplementedError) as context:
            Pace2PaceMasterRequest('this', {'is': 'a test'}, version=0.2)

        self.assertEqual('Your installed version support only version 0.10 and down', 
            context.exception.args[0])

    def test_to_json(self):
        genreq = Pace2PaceMasterRequest('this', {'is': 'a test'})
        self.assertRegex(genreq.to_json(), 
            '{"Pace2Pace": {"version": 0.1, "action": "this", "data": {"is": "a test"}, "timestamp": [0-9]+}}')
    
    def test_send_to_master_via_file(self):
        genreq = Pace2PaceMasterRequest('this', {'is': 'a test'})
        handle, temp_sig = tempfile.mkstemp()
        try:
            genreq.send_to_master_via_file(handle)
            with open(temp_sig, 'r') as f:
                newreq = json.load(f)
                self.assertEqual(newreq['Pace2Pace']['action'], 'this')
                self.assertEqual(newreq['Pace2Pace']['data'], {'is': 'a test'})
                self.assertIsInstance(newreq['Pace2Pace']['timestamp'], int)
                self.assertEqual(newreq['Pace2Pace']['version'], 0.1)
        finally:
            os.unlink (temp_sig)

    def test_new_user_request(self):
        nu = NewUserRequest('test', 'this is a test')
        # self.assertEqual(nu.action, 'new_user')
        self.assertEqual(nu.data['Pace2Pace']['name'], 'test')
        self.assertEqual(nu.data['Pace2Pace']['comment'], 'this is a test')
        self.assertEqual(nu.version, 0.1)

class pace2pace_root_key_test(unittest.TestCase):
    def test_key(self):
        key = RootKey(TEST_PRV_KEY, TEST_PUB_KEY, 'test', 'test')
        self.assertEqual( key.is_key_valid(TEST_PRV_PASS), True )

        error_key = RootKey(TEST_PRV_KEY, WRONG_PUB_KEY, 'test', 'test')
        self.assertEqual( error_key.is_key_valid(TEST_PRV_PASS), False )

        with self.assertRaises(ValueError):
            RootKey(INVALID_PRV_KEY, TEST_PUB_KEY, 'test', 'test')

        with self.assertRaises(PGPDecryptionError):
            key.sign('Hello, I have been born', 'Wrong Password')

    def test_new_key(self):
        key = RootKey.new('testpass', 'testname', 'test')
        self.assertEqual( key.is_key_valid('testpass'), True )

    def test_key_chain(self):
        logger = logging.getLogger('pace2pace')
        json_data = {'private' : TEST_PRV_KEY, 'public': TEST_PUB_KEY, 'name': 'test', 'comment': 'test'}
        key1 = RootKey.from_json(json.dumps(json_data))
        self.assertEqual( key1.is_key_valid(TEST_PRV_PASS), True )
        with self.assertLogs('pace2pace', level='DEBUG') as cm:
            kc = RootKeyChain(logger, [key1])
            key2 = RootKey.new('testpass', 'testname', 'test')
            self.assertEqual( kc.add(key2, 'Worng Password'), False )
            self.assertEqual( kc.add(key2), False )
            self.assertEqual( kc.add(key2, 'testpass'), True )
            self.assertEqual (len(kc.keys), 2)

        self.assertEqual (cm.output, 
            ['INFO:pace2pace:Keychain initialized', 'INFO:pace2pace:Added key: test Not verified', 
            'ERROR:pace2pace:Failed to add key: testname', 'ERROR:pace2pace:Failed to add key: testname', 
            'INFO:pace2pace:Added key: testname'])


if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=2, exit=False)