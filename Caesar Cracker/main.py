import time

import decode
import encode
from random import randint


def get_all_possible_decode(text):
    """
    print all decrypted strings
    :param text: encrypted text
    """
    for i in range(1, 27):
        print(decode.decode(text, i))


def get_closest_decode(text):
    """
    get the most matched decoded string
    :param text: encrypted text
    :return: decrypted text
    """
    with open(
            "most common words.txt") as file:  # get common words that every english statement contain at least one of them
        commonwords = [i.replace("\n", "") for i in file.readlines()]

    prev_points = 0
    index = 1
    for i in range(1, 27):
        points = 0
        decode_result = decode.decode(text, i, True)
        for word in decode_result.split():
            if word in commonwords:
                points += 1
        if prev_points < points:
            index = i
            prev_points = points

    return decode.decode(text, index)


def start_decode(text):
    print("start decryption...")
    print("printing all possible decodes....")
    time.sleep(1)
    get_all_possible_decode(text)
    print("\nfinished decryption\n\n")
    choice = input("Do you wont me to choose closest decryption result? (y/n): ")
    if choice.lower() == "y":
        print("getting closest decryption result...:")
        print(get_closest_decode(text))
        print("===============\n----------finish----------\n===============")


with open("text.txt") as f:
    encrypted_text = ""
    for line in f.readlines():
        encrypted_text += line

choice = input("Hi this is caesar cracker program\n is text.txt file contain encrypted text? (y/n): ")
if choice.lower() == "y":
    start_decode(encrypted_text)
else:
    encrypted_text = encode.encode(encrypted_text, randint(1, 26))
    print("So my program will encrypt the string inside text.txt file and decrypted")
    print("start encrypting...")
    time.sleep(3)
    print(encrypted_text)
    print("\nfinished encryption\n")
    time.sleep(1)
    start_decode(encrypted_text)