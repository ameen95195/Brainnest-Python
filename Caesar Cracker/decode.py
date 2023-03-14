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


def decode_capital(v, key) -> int:
    """
    shift capital characters by n number
    :param v: value of char in ascii
    :param key: shift by
    :return: shifted char in ascii
    """
    if v - key <= CAPITAL_LETTER:
        k = - v + key + CAPITAL_LETTER
        k %= BASE_COUNT
        return CAPITAL_Z - k

    return v - key


def decode_small(v, key) -> int:
    """
        shift small characters by n number
        :param v: value of char in ascii
        :param key: shift by
        :return: shifted char in ascii
        """
    if v - key <= SMALL_LETTER:
        k = - v + key + SMALL_LETTER
        k %= BASE_COUNT
        return SMALL_Z - k

    return v - key


def decode(text, key, delsymbols=False):
    """
    decode text by Caesar sphire method
    :param text: the text that want to decrypt
    :param key: the key of decryption
    :param delsymbols: delete other data that's not character default is False
    :return: decrypted text
    """
    decoded_text = ""
    for c in text:
        value = ord(c)
        if ischr(value):  # check if it`s character
            if value > CAPITAL_LETTER:  # mean's this char is capital
                decoded_text += chr(decode_capital(value, key))
            else:
                decoded_text += chr(decode_small(value, key))

        elif delsymbols:
            decoded_text += " "
        else:  # if not char it will keep it as it`s
            decoded_text += chr(value)

    return decoded_text
