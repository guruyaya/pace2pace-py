import sys
import os
import json
from logging import Logger

import pgpy
from pgpy.constants import (
    PubKeyAlgorithm, KeyFlags, HashAlgorithm,
    SymmetricKeyAlgorithm, CompressionAlgorithm)

VERSION = 0.1

class RootKey():
    def __init__(self, private: str, public: str, name :str='', comment: str=''):
        self.private = pgpy.PGPKey()
        self.private.parse(private)
        
        self.public = pgpy.PGPKey()
        self.public.parse(public)

        self.name = name
        self.comment = comment

    def sign(self, data: str, password: str = None) -> str:
        with self.private.unlock(password):
            pgp_message = pgpy.PGPMessage.new(data)
            pgp_message |= self.private.sign(pgp_message)
            return str( pgp_message.signatures[0] )

    def verify(self, data: str, signature: str):
        return bool( self.public.verify(data, pgpy.PGPSignature.from_blob(signature)) )

    def is_key_valid(self, password) -> bool:
        test_str = 'This is a test'
        try:
            signature = self.sign(test_str, password)
            return self.verify(test_str, signature)
        except (pgpy.errors.PGPDecryptionError, pgpy.errors.PGPError):
            return False

    def to_json(self):
        return json.dumps(dict(self))

    def __repr__(self):
        return "<RootKey name: {}>".format(self.name)

    @staticmethod
    def from_dict(dict):
        return RootKey(dict['private'], dict['public'], dict.get('name', ''), dict.get('comment', ''))

    @staticmethod
    def from_json(json_data):
        return RootKey.from_dict(json.loads(json_data))

    @staticmethod
    def new(password: str, name: str, comment: str):
        key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
        uid = pgpy.PGPUID.new('Pace2Pacekey')
        key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                        hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
                        ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
                        compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed])

        key.protect(password, SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)
        return RootKey(str(key), str(key.pubkey), name, comment)

class RootKeyChain():
    def __init__(self, logger: Logger,  keys: dict=[]):
        self.keys = []
        self.logger = logger
        self.logger.info("Keychain initialized")

        for key in keys:
            self.add(key, is_skip_validation=True)

    def add(self, key, password='', is_skip_validation=False):
        if is_skip_validation or key.is_key_valid(password):
            self.logger.info('Added key: {}{}'.format(key.name, ' Not verified' if is_skip_validation else ''))
            self.keys.append(key)
            return True

        self.logger.error('Failed to add key: {}'.format(key.name))
        return False
        
class Pace2PaceKeychainDirLoader():
    def __init__(self, directory=None, logger=None):
        self.directory = directory
        self.logger = logger
        self.keychain = []

    def load(self):
        if not os.access(self.directory, os.W_OK):
            self.logger.warning('Will not be able to write new keys')
        
        for entry in os.scandir(self.directory):
            try:
                jdata = json.load(entry.path)
            except Exception as e:
                self.logger.error('Could not load: {}. Error: {}', entry.path, e.__name__)






