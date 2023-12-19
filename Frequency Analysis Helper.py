#!/usr/bin/env python3
import enum
import re

import colorama

from util import clear_screen

CIPHER_TEXT = """
GSZES GNUBE SZGUG SNKGX CSUUE QNZOQ EOVJN VXKNG XGAHS
AWSZZ BOVUE SIXCQ NQESX NGEUG AHZQA QHNSP CIPQA OIDLV
JXGAK CGJCG SASUB FVQAV CIAWN VWOVP SNSXV JGPCV NODIX
GJQAE VOOXC SXXCG OGOVA XGNVU BAVKX QZVQD LVJXQ EXCQO
VKCQG AMVAX VWXCG OOBOX VZCSO SPPSN VAXUB DVVAX QJQAJ
VSUXC SXXCV OVJCS NSJXV NOJQA MVBSZ VOOSH VSAWX QHGMV
GWVSX CSXXC VBSNV ZVNVN SAWQZ ORVXJ CVOQE JCGUW NVA
"""


class Operation(enum.IntEnum):
    SUBSTITUTE = enum.auto()
    UNDO = enum.auto()
    VIEW_CURRENT_STATE_DENSE = enum.auto()
    VIEW_CURRENT_STATE_COLORED = enum.auto()


def find_all(string, substring, case_sensitive=False):
    if not case_sensitive:
        string = string.lower()
        substring = substring.lower()

    return [i for i, _ in enumerate(string) if string.startswith(substring, i)]


def operation_substitute(state):
    pattern = input("Please specify the pattern: ").strip()
    cipher_letters, key_letters = pattern.upper().split(":")
    char_sequence = [*state["undo_stack"][-1]]

    for cipher_letter, key_letter in zip(cipher_letters, key_letters):
        for index in find_all(state["cipher_text"], cipher_letter):
            char_sequence[index] = key_letter

    state["undo_stack"].append("".join(char_sequence))
    return lambda: print(f"Substitute {cipher_letters} to {key_letters}")


def operation_undo(state):
    if len(state["undo_stack"]) < 2:
        return "Already the initial state"

    state["undo_stack"].pop()
    return lambda: print("Operation undone")


def operation_view_current_state_dense(state):
    return lambda: print(re.sub(r"\s+", "", state["undo_stack"][-1]))


def operation_view_current_state_colored(state):
    def closure(cipher_text, plain_text):
        for c, p in zip(cipher_text, plain_text):
            if p == "_":
                print(colorama.Fore.RED + c, end="")
            else:
                print(colorama.Fore.GREEN + p, end="")
        print(colorama.Style.RESET_ALL)

    return lambda: closure(state["cipher_text"], state["undo_stack"][-1])


OPERATION_MAP = {
    Operation.SUBSTITUTE: {
        "description": "Substitute characters",
        "entry": operation_substitute
    },
    Operation.UNDO: {
        "description": "Undo a substitution",
        "entry": operation_undo
    },
    Operation.VIEW_CURRENT_STATE_DENSE: {
        "description": "View current state without blank characters",
        "entry": operation_view_current_state_dense
    },
    Operation.VIEW_CURRENT_STATE_COLORED: {
        "description": "View current state with color",
        "entry": operation_view_current_state_colored
    }
}


def main():
    colorama.init()

    state = {
        "cipher_text": CIPHER_TEXT,
        "undo_stack": [re.sub(r"\w", "_", CIPHER_TEXT)]
    }

    callback = lambda: None
    while True:
        clear_screen()
        callback()

        print("Cipher text")
        print(state["cipher_text"])
        print("Current solving state")
        print(state["undo_stack"][-1])

        for key, value in OPERATION_MAP.items():
            print(f"{int(key)}: {value['description']}")
        choice = input("Please select an operation: ")
        try:
            choice = Operation(int(choice))
            if choice < 1 or choice > len(OPERATION_MAP):
                continue
            callback = OPERATION_MAP[choice]["entry"](state)
        except Exception as e:
            callback = (lambda e: lambda: print(e))(e)


if __name__ == "__main__":
    main()
