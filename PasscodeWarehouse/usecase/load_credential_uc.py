import logging
import threading

from PasscodeWarehouse.domain.adapterinterface import ICredentialRepo
from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo


def invoke():
    thread = threading.Thread(target=_load_credentials)
    thread.start()


def _load_credentials():
    # Read all the credentials from file, and decrypt them into memory
    logging.debug("I'm about to load.")
    credentialRepo: ICredentialRepo = LocalFileCredentialRepo()
    logging.debug("Load credentials complete.")
