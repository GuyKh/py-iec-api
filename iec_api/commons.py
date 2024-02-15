import re


def add_jwt_to_headers(headers, token) -> dict:
    """
    Add JWT token to the headers' dictionary.
    Args:
    headers (dict): The headers dictionary to be modified.
    token (str): The JWT token to be added to the headers.
    Returns:
    dict: The modified headers dictionary with the JWT token added.
    """
    headers["Authorization"] = f"Bearer {token}"
    return headers


PHONE_REGEX: str = '^(+972|0)5[0-9]{8}$'


def check_phone(phone):
    """
    Check if the phone number is valid.
    Args:
    phone (str): The phone number to be checked.
    Returns:
    bool: True if the phone number is valid, False otherwise.
    """
    if not phone or not re.match(PHONE_REGEX, phone):
        raise ValueError("Invalid phone number")


def is_valid_israeli_id(id_number: str | int) -> bool:
    """
    Check if the ID number is valid.
    Args:
    id_number (str): The ID number to be checked.
    Returns:
    bool: True if the ID number is valid, False otherwise.
    """

    id_str = str(id_number).strip()
    if len(id_str) > 9 or not id_str.isdigit():
        return False
    id_str = id_str.zfill(9)
    return sum(
        (int(digit) if i % 2 == 0 else int(digit) * 2 if int(digit) * 2 < 10 else int(digit) * 2 - 9) for i, digit
        in enumerate(id_str)) % 10 == 0

