import re

from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo
from PasscodeWarehouse.domain.model.credential_item import CredentialItem


# Returns a dictionary with clear password text
def invoke(website_keyword: str) -> dict[str, CredentialItem]:
    all_credentials = LocalFileCredentialRepo().clear_text_dict

    return {key: value for key, value in all_credentials.items()
            if re.search(website_keyword, key, re.IGNORECASE)}
