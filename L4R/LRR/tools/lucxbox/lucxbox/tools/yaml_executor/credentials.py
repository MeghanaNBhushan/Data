from abc import ABC
from getpass import getpass, getuser
import os


class Credential(ABC):
    DEFAULT_CREDENTIAL_ID = None

    def __init__(self, credential_id):
        self.credential_id = credential_id


class PasswordCredential(Credential):
    DEFAULT_CREDENTIAL_ID = 'LUCXPASSWORD'

    def __init__(self, credential_id, username, password):
        super().__init__(credential_id)
        self.username = username
        self.password = password

    @staticmethod
    def parse(arg):
        items = arg.split(':')

        if len(items) == 2:
            credential_id = PasswordCredential.DEFAULT_CREDENTIAL_ID
            username, password = items
        else:
            credential_id, username, password = items

        return PasswordCredential(credential_id, username, password)


class SshCredential(Credential):
    DEFAULT_CREDENTIAL_ID = 'LUCXSSH'

    def __init__(self, credential_id, username, key_file):
        super().__init__(credential_id)
        self.username = username
        self.key_file = key_file

        if not key_file == "-" and not os.path.isfile(key_file):
            raise IOError('Could not find private SSH key file "' + key_file + '"')

    @staticmethod
    def parse(arg):
        credential_id, username, key_file = arg.split(':')
        return SshCredential(credential_id, username, key_file)


class CredentialManager:
    def __init__(self):
        self.map = {}

    def add(self, credential):
        self.map[credential.credential_id] = credential

    def get_password_credential(self, credential_id):
        credential = self.map.get(credential_id)

        if credential is None:
            username = input("Username for credential '" + credential_id + "' (default " + getuser() + "):\n") or getuser()
            password = getpass("Password for credential '" + credential_id + "':\n")

            credential = PasswordCredential(credential_id, username, password)
            self.map[credential_id] = credential

        if not isinstance(credential, PasswordCredential):
            raise TypeError('Requested credential does not represent a password')

        return credential

    def get_ssh_credential(self, credential_id):
        credential = self.map.get(credential_id)

        if credential is None:
            username = (input("Username for SSH credential '" + credential_id + "' (default " + getuser() + "):\n") or
                        getuser())
            key_file = input("Path to private SSH key for credential '" + credential_id + "':\n")

            credential = SshCredential(credential_id, username, key_file)
            self.map[credential_id] = credential

        if not isinstance(credential, SshCredential):
            raise TypeError('Requested credential does not represent a SSH key')

        return credential
