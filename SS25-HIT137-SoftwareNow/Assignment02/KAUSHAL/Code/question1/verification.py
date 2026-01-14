# Compare raw_text.txt with decrypted_text.txt

def verification(raw_file, decrypted_file):
    """
    Rule:
        - If raw_text == decrypted_text then successfully verified otherwise not
    Task:
        - Compares "raw_text.txt" with "decrypted_text.txt" and prints whether the decryption was
          successful or not
        - Throw exception if there is any error
    Parameters(2):
        - raw_file, the original file which was encrypted
        - decrypted_file, the file which was decrypted from encrypted file 
    """
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
