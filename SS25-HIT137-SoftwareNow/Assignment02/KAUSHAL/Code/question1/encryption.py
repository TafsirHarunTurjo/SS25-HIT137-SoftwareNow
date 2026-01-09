def encryption(shift1, shift2, base_dir):
    """
        - Each letter is divided into halves: a-m, n-z, A-M, N-Z.
        - To keep letters inside their original half after shifting, we use % 13.
          This ensures reversible encryption so that raw_text == decrypted_text.
        - Without % 13, letters could move to the other half, breaking the original rule.
    """
    try:
        reading_file = base_dir / "raw_text.txt"   
        with open(reading_file, 'r', encoding= 'utf-8') as file:
            raw_content = file.read()

        encrypt_result = ""

        for char in raw_content:
            if char.isalpha():

                # Lowercase a-m shift forward by shift1*shift2 
                if char in "abcdefghijklm":
                    base = ord('a')
                    shift = (shift1 * shift2)
                    encrypt_result += chr((ord(char) - base + shift) % 13 + base)

                # Lowercase n-z shift backward by shift1+shift2 
                elif char in "nopqrstuvwxyz":
                    base = ord('n')
                    shift = (shift1 + shift2) 
                    encrypt_result += chr((ord(char) - base - shift) % 13 + base)

                # Uppercase A-M shift backward by shift1 (mod 13)
                elif char in "ABCDEFGHIJKLM":
                    base = ord('A')
                    shift = shift1
                    encrypt_result += chr((ord(char) - base - shift) % 13 + base)

                # Uppercase N-Z shift forward by shift2^2 (mod 13)
                elif char in "NOPQRSTUVWXYZ":
                    base = ord('N')
                    shift = shift2 ** 2 
                    encrypt_result += chr((ord(char) - base + shift) % 13 + base)

            else:
                # Non-letters unchanged
                encrypt_result += char
        writing_file = base_dir / "encrypted_text.txt"  
        with open(writing_file, 'w', encoding= 'utf-8') as file:
            file.write(encrypt_result)

        print(f'Encryption completed! Encrypted text saved to {writing_file}.')

    except FileNotFoundError:
        print("Error: raw_text.txt not found.")
    except Exception as e:
        print("An unexpected error occurred:", e)



