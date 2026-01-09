def decryption(shift1, shift2, base_dir):
    try:
        read_encrytion = base_dir / "encrypted_text.txt" 
        with open(read_encrytion , 'r', encoding= 'utf-8') as file:
            encrypted_content = file.read()

        decrypt_result = ""

        for char in encrypted_content:
            if char.isalpha():
                # Lowercase a-m shift backward
                if char in "abcdefghijklm":
                    base = ord('a')
                    shift = (shift1 * shift2) 
                    decrypt_result += chr((ord(char) - base - shift) % 13 + base)

                # Lowercase n-z shift forward
                elif char in "nopqrstuvwxyz":
                    base = ord('n')
                    shift = (shift1 + shift2)
                    decrypt_result += chr((ord(char) - base + shift) % 13 + base)

                # Uppercase A-M shift forward
                elif char in "ABCDEFGHIJKLM":
                    base = ord('A')
                    shift = shift1 
                    decrypt_result += chr((ord(char) - base + shift) % 13 + base)

                # Uppercase N-Z shift backward
                elif char in "NOPQRSTUVWXYZ":
                    base = ord('N')
                    shift = (shift2 ** 2) 
                    decrypt_result += chr((ord(char) - base - shift) % 13 + base)

            else:
                # Non-letters unchanged
                decrypt_result += char
        write_decryption = base_dir / "decrypted_text.txt" 
        with open(write_decryption, 'w', encoding= 'utf-8') as file:
            file.write(decrypt_result)

        print(f'Decryption completed! Decrypted text saved to {write_decryption}.')

    except FileNotFoundError:
        print("Error: encrypted_text.txt not found.")
    except Exception as e:
        print("An unexpected error occurred:", e)




