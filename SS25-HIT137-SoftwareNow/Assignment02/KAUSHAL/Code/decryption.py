def decryption(shift1, shift2):
    try:
        with open('encrypted_text.txt', 'r') as file:
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

        with open('decrypted_text.txt', 'w') as file:
            file.write(decrypt_result)

        print('Decryption completed! Decrypted text saved to "decrypted_text.txt".')

    except FileNotFoundError:
        print("Error: encrypted_text.txt not found.")
    except Exception as e:
        print("An unexpected error occurred:", e)




