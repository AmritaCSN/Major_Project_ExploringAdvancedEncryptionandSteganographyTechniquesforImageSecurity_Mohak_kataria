'''
This program does the following:
    encrypts the text using ChaCha20, AES, DES, and RSA
    then hides it in a simple image - using Spread Spectrum
    then extract it from the image
    finally decrypts the extracted text

We analyze the performance of the encryption and decryption of the alogs
Keeping all the other paramers - text and image - unaltered.
'''
from __future__ import absolute_import, unicode_literals
from ChaCha20 import Chacha20
from hashlib import sha256
from Crypto import Random
from aes import AESCipher
from des import DESCipher
from stegano import lsb
import base64
import threading
import textwrap
import hashlib
import random
import os.path
import base64
import time
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from infoentrophy import information_entropy
from rsa_python import rsa

def embed(cover_image, secret_data):
    stegoed_image = stegoed_image = cover_image.split(".")[-2]+ "_stegoed.png"
    cover_image = cv2.imread(cover_image)
    # Converting  plaintext  to binary string
    binary_data = int.from_bytes(secret_data, byteorder='big')
    bin_data= bin(binary_data)[2:]  # Remove the '0b' prefix
    # Generating the pseudoradom image
    height=cover_image.shape[0]
    width=cover_image.shape[1]
    cha=cover_image.shape[2]
    sequence_length = height*width*cha
    sequence = [random.randint(0, 1) for i in range(sequence_length)]
    # embedding the ciphertext into image
    index = 0
    for row in range(height):
        for col in range(width):
            for channel in range(cha):
                            if index < len(bin_data):
                                # Converting the  pixel value to binary string
                                binary_pixel = format(cover_image[row, col, channel], '08b')

                                # updating the  LSB of pixel value
                                modified_pixel = binary_pixel[:-1] + bin_data[index] + str(sequence[index])

                                # converting modified pixel value back to integer
                                cover_image[row, col, channel] = int(modified_pixel, 2) % 256

                                index += 1
                            else:
                                break
            else:
                continue
            break
        else:
            continue
        break

    # Saving the stegoed-image

    cv2.imwrite(stegoed_image, cover_image) #we have to change this for every image to add stegoed images, tried but getting errors so working manually.

def dembed(input_image):
    input_image = cv2.imread(input_image)
    bin_data = ''
    stego_height=input_image.shape[0]
    stego_width=input_image.shape[1]
    stego_cha=input_image.shape[2]
    for row in range(stego_height):
        for col in range(stego_width):
            for channel in range(stego_cha):
                # Converting pixel value to binary string
                binary_pixel = format(input_image[row, col, channel], '08b')

                # Extracting binary string of pixel 
                bin_data += binary_pixel[-2:]

    # Convert binary string to ASCII string
    secret_data = ''
    for i in range(0, len(bin_data), 8):
                secret_data += chr(int(bin_data[i:i+8], 2))

def main(path):
    stegoed_image = path.split(".")[-2]+ "_stegoed.png"
    message=''
    enc_time=0.0

    
    for mode in ['AES', 'DES', 'ChaCha20','RSA']:
        print(f"================== Using {mode} ==============================")
        print(f"Msg Len\t\tSteghide Time\t\t\tStegunhide Time")
        
        for i in range(1, 12, 1):
            key='12345678'
            enc_time=0.0
            message='a'*(2**i)
            
            if mode=='AES':

                aes_algo=AESCipher(key)

                enc_start_time=time.time()
                encrypted_data=aes_algo.encrypt(message)
                enc_time = time.time()-enc_start_time

                # Loading the  cover image
                embed(path, encrypted_data)
                # Saving the stegoed-image
                dembed(path) 
                # now we extract the data and check the time
                dec_start = time.time()
                dec_time = time.time() - dec_start
                secret_data=encrypted_data.decode()
                decrypted_data=aes_algo.decrypt(secret_data)
                print(f"{len(message)}\t\t{enc_time}\t\t{dec_time}")
            
            elif mode=='DES':
                des_object=DESCipher(key)

                enc_start_time=time.time()
                encrypted_data=des_object.encrypt(message)
                enc_time = time.time()-enc_start_time

                # Loading the cover image
                secret_data=encrypted_data
                
                embed(path,secret_data)
                dembed(path)
 
                # now we extract the data and check the time
                dec_start = time.time()
                dec_time = time.time() - dec_start
                print(f"{len(message)}\t{enc_time}\t{dec_time}")
            
            elif mode=='RSA':
                key_pair=rsa.generate_key_pair(1024)
                enc_start_time=time.time()
                encrypted_data=rsa.encrypt(message,key_pair["public"], key_pair["modulus"])
                # Loading the cover image
                cover_image = cv2.imread(path)
                secret_data=encrypted_data
                enc_time=time.time()-enc_start_time
                # Convert the plaintext to binary string
                binary_data = ''.join(format(ord(char), '08b') for char in secret_data)
                # Generating the pseudo-random sequence
                height=cover_image.shape[0]
                width=cover_image.shape[1]
                cha=cover_image.shape[2]
                sequence_length = height * width * cha
                sequence = [random.randint(0, 1) for i in range(sequence_length)]
                # Embedding the ciphertext into the cover imge
                index = 0
                for row in range(height):
                    for col in range(width):
                        for channel in range(cha):
                            if index < len(binary_data):
                    # Converting the pixel value to binary string
                                binary_pixel = format(cover_image[row, col, channel], '08b')

                    # updating the pixel value 
                                modified_pixel = binary_pixel[:-1] + binary_data[index] + str(sequence[index])

                    # Converting the above modified pixel value back to integer 
                                cover_image[row, col, channel] = int(modified_pixel, 2) % 256
                                index += 1
                            else:
                                break
                        else:
                            continue
                        break
                    else:
                        continue
                    break

                # Saving the updated image as  stegoed-image
                stegoed_image = path.split(".")[-2]+ "_stegoed.png"
                cv2.imwrite(stegoed_image, cover_image)
            
                # Loading the  stegoed-image
                stegoed_image = cv2.imread(stegoed_image)

                # Extract ciphertext  from stego-image
                binary_data = ''
                stego_height=stegoed_image.shape[0]
                stego_width=stegoed_image.shape[1]
                stego_cha=stegoed_image.shape[2]
                # loops to dembeed the ciphertext in the images. Convert ciphertext to binary. Row and column and then channel.             
                for row in range(stego_height):
                    for col in range(stego_width):
                        for channel in range(stego_cha):
                # Converting the pixel value to binary string
                            binary_pixel = format(stegoed_image[row, col, channel], '08b')
                # extracting the pixel value
                            binary_data += binary_pixel[-2:]
                # Converting the above receieved binary string to ASCII string
                secret_data = ''
                for i in range(0, len(binary_data), 8):
                    secret_data += chr(int(binary_data[i:i+8], 2))
                enc_time = time.time()-enc_start_time
                
                # now we extract the data and check the time
                dec_start = time.time()
                decrypted_data=rsa.decrypt(encrypted_data, key_pair["private"], key_pair["modulus"])
                dec_time = time.time() - dec_start
                #print("decrypted data is: ",decrypted_data)
                print(f"{len(message)}\t\t{enc_time}\t\t{dec_time}")
            
            elif mode=='ChaCha20':

                enc_start_time=time.time()
                encrypted_data=Chacha20.encrypt(message)
                enc_time = time.time()-enc_start_time
                # Loading the cover image
                secret_data=encrypted_data.encode('utf-8')
                #print("the secret data is :", secret_data)
                #print("the type of secret data is :", type(secret_data))
                embed(path,secret_data)
                dembed(path) 
                # now we extract the data and check the time
                dec_start = time.time()
                dec_time = time.time() - dec_start
                print(f"{len(message)}\t{enc_time}\t{dec_time}")

if __name__ == '__main__':
    path = ''
    while(not path):
        path = input("Enter file to hide text into : ")
    main(path)
    # Load original and stego images
    original_image = cv2.imread(path)
    stegoed_image = path.split(".")[-2]+ "_stegoed.png"
    stegoed_image = cv2.imread(stegoed_image)
    # Calculate MSE and PSNR
    mse = np.mean((original_image - stegoed_image) ** 2)
    if mse == 0:
       psnr = 100
    else:
      max_pixel_value = 255.0
      psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    # Print MSE and PSNR
    print(f"MSE: {mse}")
    print(f"PSNR: {psnr}")
    #computing histogram for images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(original_image.ravel(), bins=256, range=(0, 256))
    plt.title('Histogram of Original Image')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 2, 2)
    plt.hist(stegoed_image.ravel(), bins=256, range=(0, 256))
    plt.title('Histogram of Steganographic Image')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.show()
                
    #computing the separate histograms for RGB of original image
    # Split the image into its red, green, and blue channels
    b, g, r = cv2.split(original_image)
    
    # Calculate and plot the histograms of the red, green, and blue channels separately
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.hist(r.ravel(), bins=256, range=(0, 256), color='r')
    plt.title('Histogram of Red Channel')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 3, 2)
    plt.hist(g.ravel(), bins=256, range=(0, 256), color='g')
    plt.title('Histogram of Green Channel')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 3, 3)
    plt.hist(b.ravel(), bins=256, range=(0, 256), color='b')
    plt.title('Histogram of Blue Channel')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.show()
    
    #computing the separate histograms for RGB of stego image
    # Split the image into its red, green, and blue channels
    b, g, r = cv2.split(stegoed_image)
    
    # Calculate and plot the histograms of the red, green, and blue channels separately
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.hist(r.ravel(), bins=256, range=(0, 256), color='r')
    plt.title('Stego of Red Channel')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 3, 2)
    plt.hist(g.ravel(), bins=256, range=(0, 256), color='g')
    plt.title('Stego of Green Channel')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 3, 3)
    plt.hist(b.ravel(), bins=256, range=(0, 256), color='b')
    plt.title('Stego of Blue Channel ')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.show()

    stegoed_image = path.split(".")[-2]+ "_stegoed.png"
    stego_entropy = information_entropy(stegoed_image)
    print('Stego image information entropy:', stego_entropy)
