# Compare raw_text.txt with decrypted_text.txt

def verification(raw_file, decrypted_file):
    try:
        with open(raw_file, 'r', encoding='utf-8') as f1, open(decrypted_file, 'r', encoding='utf-8') as f2:
            raw_text = f1.read()
            decrypted_text = f2.read()

        if raw_text == decrypted_text:
            print("Decryption successfully verified! Decrypted text matches raw text!")
        else:
            print("Decryption can't be verified! Decrypted text does not match raw text.")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print("An unexpected error occurred during comparison:", e)
