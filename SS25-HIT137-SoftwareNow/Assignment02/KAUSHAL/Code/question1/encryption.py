def encryption(shift1, shift2, base_dir):
    """
    Rule:
        - Each letter is divided into halves: a-m, n-z, A-M, N-Z
        - To keep letters inside their original half after shifting, we use % 13,
          This ensures reversible encryption so that raw_text == decrypted_text
        - Without % 13, letters could move to the other half, breaking the original rule
    Task:
        - Reads from "raw_text.txt" and writes encrypted content to "encrypted_text.txt"
        - Throw exception if there is any error
    Parameters(3):
        - shift1 and shift2 for shifting the characters in raw text
        - base_dir to get the base file path

    """
    try:
        reading_file = base_dir / "raw_text.txt"   
        with open(reading_file, 'r', encoding= 'utf-8') as file:
            raw_content = file.read()

        encrypt_result = ""

        for char in raw_content:
            if char.isalpha():

                # lowercase a-m shift forward by shift1*shift2 
                if char in "abcdefghijklm":
                    base = ord('a')
                    shift = (shift1 * shift2)
                    encrypt_result += chr((ord(char) - base + shift) % 13 + base)

                # lowercase n-z shift backward by shift1+shift2 
                elif char in "nopqrstuvwxyz":
                    base = ord('n')
                    shift = (shift1 + shift2) 
                    encrypt_result += chr((ord(char) - base - shift) % 13 + base)

                # uppercase A-M shift backward by shift1 
                elif char in "ABCDEFGHIJKLM":
                    base = ord('A')
                    shift = shift1
                    encrypt_result += chr((ord(char) - base - shift) % 13 + base)

                # uppercase N-Z shift forward by shift2^2 
                elif char in "NOPQRSTUVWXYZ":
                    base = ord('N')
                    shift = shift2 ** 2 
                    encrypt_result += chr((ord(char) - base + shift) % 13 + base)

            else:
                # non-letters: keep as it is (no change)
                encrypt_result += char
        writing_file = base_dir / "encrypted_text.txt"  
        with open(writing_file, 'w', encoding= 'utf-8') as file:
            file.write(encrypt_result)

        print(f'Encryption completed! Encrypted text saved to {writing_file}.')

    except FileNotFoundError:
        print("Error: raw_text.txt not found.")
    except Exception as e:
        print("An unexpected error occurred:", e)



