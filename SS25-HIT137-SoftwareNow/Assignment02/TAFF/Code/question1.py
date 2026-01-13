# # question1.py

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
