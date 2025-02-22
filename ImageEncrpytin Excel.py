import time
import hashlib
from PIL import Image
import numpy as np
import pandas as pd
from ecdsa import SigningKey, SECP256k1

def generate_ecc_keys():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def ecc_encrypt_decrypt(data, private_key, public_key):
    try:
        signature = private_key.sign(data)
        
        try:
            public_key.verify(signature, data)
        except Exception as e:
            print(f"Signature verification failed: {e}")

        return signature.hex() 
    except Exception as e:
        print(f"Error in ecc_encrypt_decrypt: {e}")
        return None

def process_images_for_multiple_users(num_users=150):
    users_data = [] 
    
    for i in range(num_users):
        print(f"\nProcessing User {i+1}/{num_users}")

        image_path = input("Enter the image path (or type 'exit' to stop): ").strip()
        if image_path.lower() == "exit":
            print(f"\nProcess stopped after {i} users.")
            break

        try:
            print("Opening and processing image...")
            image = Image.open(image_path).convert("RGB")
            pixels = np.array(image)
            print(f"Image loaded with shape: {pixels.shape}")
        except Exception as e:
            print(f"Error opening image: {e}")
            continue

        print("Generating ECC keys...")
        private_key, public_key = generate_ecc_keys()
        print("ECC keys generated successfully.")

        print("Hashing image data...")
        image_bytes = pixels.tobytes()
        image_hash = hashlib.sha256(image_bytes).digest()

        print("Encrypting image hash...")
        start_time = time.time()
        encrypted_hash = ecc_encrypt_decrypt(image_hash, private_key, public_key)
        encryption_time = time.time() - start_time

        if encrypted_hash:
            print(f"Encryption successful! Time taken: {encryption_time:.5f} seconds")
        else:
            print("Encryption failed.")

        name = input(f"Enter name for User {i+1} (or type 'exit' to stop): ").strip()
        if name.lower() == "exit":
            print(f"\nProcess stopped after {i} users.")
            break
        
        reg_no = input(f"Enter registration number for User {i+1} (or type 'exit' to stop): ").strip()
        if reg_no.lower() == "exit":
            print(f"\nProcess stopped after {i} users.")
            break

        users_data.append([i + 1, name, reg_no, encrypted_hash, f"{encryption_time:.5f} sec"])

        print(f"User {i+1} processed successfully. Moving to the next user...")

    df = pd.DataFrame(users_data, columns=["User ID", "Name", "Reg No", "Encrypted Hash", "Encryption Time"])
    df.to_excel("encrypted_users.xlsx", index=False)
    print("\nProcess completed. All users processed successfully.")
    print("Data saved in 'encrypted_users.xlsx'.")

process_images_for_multiple_users(150)
