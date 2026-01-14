def decryption(shift1, shift2, base_dir):
    """
    Rule(As in encryption except sign(+,-) interchange):
        - Each letter is divided into halves: a-m, n-z, A-M, N-Z
        - To keep letters inside their original half after shifting, we use % 13
          This ensures reversible encryption so that raw_text == decrypted_text
        - Without % 13, letters could move to the other half, breaking the original rule
    Task:
        - Reads from "encrypted_text.txt" and writes the decrypted content to "decrypted_text.txt"
        - Throw exception if there is any error
    Parameters(3):
        - shift1 and shift2 for shifting the characters in encrypted text
        - base_dir to get the base file path
    """

    try:
        read_encrytion = base_dir / "encrypted_text.txt" 
        with open(read_encrytion , 'r', encoding= 'utf-8') as file:
            encrypted_content = file.read()

        decrypt_result = ""

        for char in encrypted_content:
            if char.isalpha():
                # lowercase a-m shift backward by shift1*shift2 
                if char in "abcdefghijklm":
                    base = ord('a')
                    shift = (shift1 * shift2) 
                    decrypt_result += chr((ord(char) - base - shift) % 13 + base)

                # lowercase n-z shift forward by shift1+shift2 
                elif char in "nopqrstuvwxyz":
                    base = ord('n')
                    shift = (shift1 + shift2)
                    decrypt_result += chr((ord(char) - base + shift) % 13 + base)

                # uppercase A-M shift forward by shift1 
                elif char in "ABCDEFGHIJKLM":
                    base = ord('A')
                    shift = shift1 
                    decrypt_result += chr((ord(char) - base + shift) % 13 + base)

                # uppercase N-Z shift backward  by shift2^2 
                elif char in "NOPQRSTUVWXYZ":
                    base = ord('N')
                    shift = (shift2 ** 2) 
                    decrypt_result += chr((ord(char) - base - shift) % 13 + base)

            else:
                # non-letters: keep as it is (no change)
                decrypt_result += char
        write_decryption = base_dir / "decrypted_text.txt" 
        with open(write_decryption, 'w', encoding= 'utf-8') as file:
            file.write(decrypt_result)

        print(f'Decryption completed! Decrypted text saved to {write_decryption}.')

    except FileNotFoundError:
        print("Error: encrypted_text.txt not found.")
    except Exception as e:
        print("An unexpected error occurred:", e)




