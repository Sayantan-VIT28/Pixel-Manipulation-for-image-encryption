from PIL import Image 
import numpy as np 
def encrypt_image(image_path, key):
    img = Image.open(image_path)
    img_array = np.array(img)  
    encrypted_array = (img_array + key) % 256
    encrypted_img = Image.fromarray(np.uint8(encrypted_array))
    encrypted_img.save("encrypted_image.png")
    print("Image encrypted and saved as 'encrypted_image.png'.")

def decrypt_image(encrypted_image_path, key):
    img = Image.open(encrypted_image_path)
    img_array = np.array(img)
    decrypted_array = (img_array - key) % 256
    decrypted_img = Image.fromarray(np.uint8(decrypted_array))
    decrypted_img.save("decrypted_image.png")
    print("Image decrypted and saved as 'decrypted_image.png'.")

def main():
    print("Welcome to the Image Encryption Tool!")
    while True:
        print("\nMenu:")
        print("1. Encrypt an Image")
        print("2. Decrypt an Image")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            image_path = input("Enter the path of the image to encrypt: ")
            key = int(input("Enter the encryption key (integer): "))
            encrypt_image(image_path, key)
        elif choice == "2":
            encrypted_image_path = input("Enter the path of the encrypted image: ")
            key = int(input("Enter the decryption key (integer): "))
            decrypt_image(encrypted_image_path, key)
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
