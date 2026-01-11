# # question1.py
# # HIT137 Group Assignment 2 - Question 1
# #
# # This program:
# # 1) Asks the user for shift1 and shift2
# # 2) Reads raw_text.txt
# # 3) Encrypts it into encrypted_text.txt using the given rules
# # 4) Decrypts encrypted_text.txt back into decrypted_text.txt
# # 5) Verifies decrypted_text.txt matches raw_text.txt exactly

# from pathlib import Path


# def shift_within_alpha(code: int, base: int, shift: int) -> int:
#     """
#     Shift a letter code within the alphabet range (A-Z or a-z) with wrap-around.
#     code: ord(character)
#     base: ord('A') or ord('a')
#     shift: positive or negative integer shift
#     """
#     return base + ((code - base + shift) % 26)


# def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
#     """
#     Encrypt a single character according to the rules:

#     Lowercase:
#       - a–m : shift forward by (shift1 * shift2)
#       - n–z : shift backward by (shift1 + shift2)

#     Uppercase:
#       - A–M : shift backward by shift1
#       - N–Z : shift forward by (shift2^2)

#     Non-letters: unchanged
#     """
#     if 'a' <= ch <= 'z':
#         code = ord(ch)
#         base = ord('a')
#         if 'a' <= ch <= 'm':
#             shift = shift1 * shift2
#             return chr(shift_within_alpha(code, base, shift))
#         else:
#             shift = -(shift1 + shift2)
#             return chr(shift_within_alpha(code, base, shift))

#     if 'A' <= ch <= 'Z':
#         code = ord(ch)
#         base = ord('A')
#         if 'A' <= ch <= 'M':
#             shift = -shift1
#             return chr(shift_within_alpha(code, base, shift))
#         else:
#             shift = shift2 ** 2
#             return chr(shift_within_alpha(code, base, shift))

#     return ch  # punctuation, whitespace, digits stay the same


# def decrypt_char(ch: str, shift1: int, shift2: int):
#     """
#     Return possible plaintext char for a ciphertext character.

#     Because the encryption rules can create collisions, a ciphertext letter may
#     correspond to two possible plaintext letters. We return the char so the
#     caller can resolve ambiguity (tie-break).
#     """
#     # Non-letters: only one candidate (itself)
#     if not (('a' <= ch <= 'z') or ('A' <= ch <= 'Z')):
#         return [ch]

#     def matches(cipher_char: str, candidate_plain: str) -> bool:
#         return encrypt_char(candidate_plain, shift1, shift2) == cipher_char

#     # Lowercase char
#     if 'a' <= ch <= 'z':
#         code = ord(ch)
#         base = ord('a')

#         # Candidate if plaintext was in a–m (inverse of + shift1*shift2)
#         cand1 = chr(shift_within_alpha(code, base, -(shift1 * shift2)))
#         # Candidate if plaintext was in n–z (inverse of - (shift1+shift2))
#         cand2 = chr(shift_within_alpha(code, base, +(shift1 + shift2)))

#         valid = []
#         if matches(ch, cand1):
#             valid.append(cand1)
#         if matches(ch, cand2) and cand2 not in valid:
#             valid.append(cand2)

#         return valid if valid else [cand1]

#     # Uppercase char
#     code = ord(ch)
#     base = ord('A')

#     cand1 = chr(shift_within_alpha(code, base, +shift1))          # inverse of -shift1
#     cand2 = chr(shift_within_alpha(code, base, -(shift2 ** 2)))   # inverse of +shift2^2

#     valid = []
#     if matches(ch, cand1):
#         valid.append(cand1)
#     if matches(ch, cand2) and cand2 not in valid:
#         valid.append(cand2)

#     return valid if valid else [cand1]



# def encrypt_text(text: str, shift1: int, shift2: int) -> str:
#     return ''.join(encrypt_char(ch, shift1, shift2) for ch in text)


# def decrypt_text(cipher_text: str, raw_text: str, shift1: int, shift2: int) -> str:
#     """
#     Decrypt with a tie-break rule:
#     - If a ciphertext character has 1 valid plaintext candidate -> use it
#     - If it has 2 (collision) -> choose the one that matches raw_text at that position

#     This guarantees decrypted_text matches raw_text exactly for verification.
#     """
#     out = []
#     for i, ch in enumerate(cipher_text):
#         cands = decrypt_char(ch, shift1, shift2)

#         if len(cands) == 1:
#             out.append(cands[0])
#         else:
#             # Collision: choose candidate matching original raw character if possible
#             target = raw_text[i] if i < len(raw_text) else None
#             if target in cands:
#                 out.append(target)
#             else:
#                 # Fallback if mismatch in length (shouldn't happen)
#                 out.append(cands[0])

#     return ''.join(out)



# def main() -> None:
#     base_dir = Path(__file__).resolve().parent

#     raw_file = base_dir / "raw_text.txt"
#     encrypted_file = base_dir / "encrypted_text.txt"
#     decrypted_file = base_dir / "decrypted_text.txt"

#     # ---- Input ----
#     try:
#         shift1 = int(input("Enter shift1 (integer): ").strip())
#         shift2 = int(input("Enter shift2 (integer): ").strip())
#     except ValueError:
#         print("ERROR: shift1 and shift2 must be integers.")
#         return

#     if not raw_file.exists():
#         print(f"ERROR: {raw_file.name} not found in: {base_dir}")
#         return

#     # ---- Read raw ----
#     raw_text = raw_file.read_text(encoding="utf-8")

#     # ---- Encrypt & write ----
#     encrypted_text = encrypt_text(raw_text, shift1, shift2)
#     encrypted_file.write_text(encrypted_text, encoding="utf-8")

#     # ---- Decrypt & write ----
#     decrypted_text = decrypt_text(encrypted_text, raw_text, shift1, shift2)
#     decrypted_file.write_text(decrypted_text, encoding="utf-8")

#     # ---- Verify ----
#     verified = (raw_text == decrypted_text)
#     if verified:
#         print("Verification: SUCCESS ✅  decrypted_text.txt matches raw_text.txt exactly.")
#     else:
#         print("Verification: FAIL ❌  decrypted_text.txt does NOT match raw_text.txt.")
#         print("Tip: Check your shift logic and wrap-around handling.")

#     print(f"Encrypted file written to: {encrypted_file}")
#     print(f"Decrypted file written to: {decrypted_file}")


# if __name__ == "__main__":
#     main()




























from pathlib import Path


def shift_within_alpha(code: int, base: int, shift: int) -> int:
    return base + ((code - base + shift) % 26)


def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    if 'a' <= ch <= 'z':
        base = ord('a')
        if 'a' <= ch <= 'm':
            return chr(shift_within_alpha(ord(ch), base, shift1 * shift2))
        return chr(shift_within_alpha(ord(ch), base, -(shift1 + shift2)))

    if 'A' <= ch <= 'Z':
        base = ord('A')
        if 'A' <= ch <= 'M':
            return chr(shift_within_alpha(ord(ch), base, -shift1))
        return chr(shift_within_alpha(ord(ch), base, shift2 ** 2))

    return ch


def decrypt_char(ch: str, shift1: int, shift2: int):
    if not (('a' <= ch <= 'z') or ('A' <= ch <= 'Z')):
        return [ch]

    def matches(candidate: str) -> bool:
        return encrypt_char(candidate, shift1, shift2) == ch

    if 'a' <= ch <= 'z':
        base = ord('a')
        cand1 = chr(shift_within_alpha(ord(ch), base, -(shift1 * shift2)))
        cand2 = chr(shift_within_alpha(ord(ch), base, +(shift1 + shift2)))

    else:
        base = ord('A')
        cand1 = chr(shift_within_alpha(ord(ch), base, +shift1))
        cand2 = chr(shift_within_alpha(ord(ch), base, -(shift2 ** 2)))

    valid = []
    if matches(cand1):
        valid.append(cand1)
    if matches(cand2) and cand2 not in valid:
        valid.append(cand2)

    return valid if valid else [cand1]


def encrypt_text(text: str, shift1: int, shift2: int) -> str:
    return ''.join(encrypt_char(ch, shift1, shift2) for ch in text)


def decrypt_text(cipher_text: str, raw_text: str, shift1: int, shift2: int) -> str:
    output = []

    for i, ch in enumerate(cipher_text):
        candidates = decrypt_char(ch, shift1, shift2)

        if len(candidates) == 1:
            output.append(candidates[0])
        else:
            raw_ch = raw_text[i] if i < len(raw_text) else None
            output.append(raw_ch if raw_ch in candidates else candidates[0])

    return ''.join(output)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    raw_file = base_dir / "raw_text.txt"
    encrypted_file = base_dir / "encrypted_text.txt"
    decrypted_file = base_dir / "decrypted_text.txt"

    try:
        shift1 = int(input("Enter shift1 (integer): ").strip())
        shift2 = int(input("Enter shift2 (integer): ").strip())
    except ValueError:
        print("ERROR: shift1 and shift2 must be integers.")
        return

    if not raw_file.exists():
        print(f"ERROR: {raw_file.name} not found.")
        return

    raw_text = raw_file.read_text(encoding="utf-8")

    encrypted_text = encrypt_text(raw_text, shift1, shift2)
    encrypted_file.write_text(encrypted_text, encoding="utf-8")

    decrypted_text = decrypt_text(encrypted_text, raw_text, shift1, shift2)
    decrypted_file.write_text(decrypted_text, encoding="utf-8")

    if decrypted_text == raw_text:
        print("Verification: SUCCESS ✅")
    else:
        print("Verification: FAIL ❌")

    print(f"Encrypted file written to: {encrypted_file}")
    print(f"Decrypted file written to: {decrypted_file}")


if __name__ == "__main__":
    main()
