from constants import *


def ischr(value: int) -> bool:
    """
    check if the ascii is character
    :param value: char in ascii
    :return: True if its char otherwise folse
    """
    if value in range(SMALL_LETTER + 1, SMALL_Z + 1) or value in range(CAPITAL_LETTER + 1, CAPITAL_Z + 1):
        return True
    return False


def encode_capital(v, key) -> int:
    """
    shift capital characters by n number
    :param v: value of char in ascii
    :param key: shift by
    :return: shifted char in ascii
    """
    if v + key > CAPITAL_Z:
        k = v + key - CAPITAL_Z
        k %= BASE_COUNT
        return CAPITAL_LETTER + k

    return v + key


def encode_small(v, key) -> int:
    """
        shift small characters by n number
        :param v: value of char in ascii
        :param key: shift by
        :return: shifted char in ascii
        """
    if v + key > SMALL_Z:
        k = v + key - SMALL_Z
        k %= BASE_COUNT
        return SMALL_LETTER + k

    return v + key


def encode(text, key):
    """
    encode text by Caesar sphire method
    :param text: the text that want to encrypt
    :param key: the key of encryption
    :return: encrypted text
    """
    encoded_text = ""
    for c in text:
        value = ord(c)
        if ischr(value):  # check if it`s character
            if value > CAPITAL_LETTER:  # mean's this char is capital
                encoded_text += chr(encode_capital(value, key))
            else:
                encoded_text += chr(encode_small(value, key))

        else:  # if not char it will keep it as it`s
            encoded_text += chr(value)

    return encoded_text
