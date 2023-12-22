from PasscodeWarehouse.domain.password_generator import generate_password


def invoke(lowercase: bool, uppercase: bool, number: bool, custom_chars: str, required_len) -> str:
    return generate_password(
        lowercase=lowercase,
        uppercase=uppercase,
        number=number,
        custom_chars=custom_chars,
        required_length=required_len
    )
