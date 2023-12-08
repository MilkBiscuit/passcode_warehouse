import re

from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo


def invoke(website_keyword: str) -> dict:
    # if read_user_backup_passcode() == "":
    #     return {}

    return _search_matched_results(website_keyword)


# Returns a dictionary with clear password text
def _search_matched_results(website_keyword: str) -> dict:
    result = {}
    dictionary = LocalFileCredentialRepo().clear_text_dict

    for key in dictionary.keys():
        if re.search(website_keyword, key, re.IGNORECASE):
            result[key] = {
                "username": dictionary[key]["username"],
                "password": dictionary[key]["password"]
            }

    return result
