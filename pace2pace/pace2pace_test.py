import unittest
import tempfile
import os
import json
from pace2pace_master_client import Pace2PaceMasterRequest, NewUserRequest

class pace2pace_test(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=2, exit=False)