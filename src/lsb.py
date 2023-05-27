'''
This program does the following:
    encrypts the text using ChaCha20, AES, DES, and RC6
    then hides it in a simple image - using LSB Embedding technique
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
import threading
import textwrap
import hashlib
import os.path
import base64
import time
import os
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from infoentrophy import information_entropy
from rsa_python import rsa
def main():
    path = ''
    while(not path):
        path = input("Enter file to hide text into : ")
    
    image_name = path.split("/")[-1]
    directory = path.replace(image_name, "")
    output_path = directory + "_stegoed_" + image_name

    # debug

    print(f"path = {path}")
    print(f"image_name = {image_name}")
    print(f"directory = {directory}")
    print(f"output_path = {output_path}")

    message=''
    enc_time=0.0
    runtime=[]
    
    for mode in ['AES', 'DES', 'ChaCha20', 'RSA']:
        print(f"================== Using {mode} ==============================")
        print(f"Msg Len\tencryption Time\t\tDecryption Time")
        
        for i in range(1, 12, 1):
            key='12345678'
            enc_time=0.0
            message='a'*(2**i)
            
            if mode=='AES':
                if os.path.isfile(output_path):
                        os.remove(output_path)

                aes_algo=AESCipher(key)

                enc_start_time=time.time()
                encrypted_data=aes_algo.encrypt(message)
                secret = lsb.hide(path, encrypted_data)
                secret.save(output_path)
                enc_time = time.time()-enc_start_time
                
                # now we extract the data and check the time
                dec_start = time.time()
                encrypted_data = lsb.reveal(output_path)
                decrypted_data = aes_algo.decrypt(encrypted_data)
                dec_time = time.time() - dec_start
                runtime.append(dec_time)

                print(f"{len(message)}\t{enc_time}\t{dec_time}")

            
            if mode=='RSA':
                if os.path.isfile(output_path):
                    os.remove(output_path)
              
                key_pair=rsa.generate_key_pair(1024)
                enc_start_time=time.time()
                encrypted_data=rsa.encrypt(message,key_pair['public'],key_pair['modulus'])
                secret=lsb.hide(path,encrypted_data)
                secret.save(output_path)
                enc_time=time.time()-enc_start_time
                # now we extract the data and check the time
                dec_start = time.time()
                encrypted_data = lsb.reveal(output_path)
                decrypted_data = rsa.decrypt(encrypted_data, key_pair['private'], key_pair['modulus'])
                dec_time = time.time() - dec_start
                runtime.append(dec_time)
                print(f"{len(message)}\t{enc_time}\t{dec_time}")
            
            elif mode=='DES':
                if os.path.isfile(output_path):
                    os.remove(output_path)                          
                des_object=DESCipher(key)

                enc_start_time=time.time()
                encrypted_data=des_object.encrypt(message)
                secret = lsb.hide(path, encrypted_data)
                secret.save(output_path)
                enc_time = time.time()-enc_start_time
                
                # now we extract the data and check the time
                dec_start = time.time()
                encrypted_data = lsb.reveal(output_path)
                decrypted_data = des_object.decrypt(encrypted_data)
                dec_time = time.time() - dec_start

                print(f"{len(message)}\t{enc_time}\t{dec_time}")

            elif mode=='ChaCha20':
                if os.path.isfile(output_path):
                        os.remove(output_path)

                enc_start_time=time.time()
                encrypted_data=Chacha20.encrypt(message)
                secret = lsb.hide(path, encrypted_data)
                secret.save(output_path)
                enc_time = time.time()-enc_start_time
                
                # now we extract the data and check the time
                dec_start = time.time()
                encrypted_data = lsb.reveal(output_path)
                decrypted_data = Chacha20.decrypt(encrypted_data)
                dec_time = time.time() - dec_start

                print(f"{len(message)}\t{enc_time}\t{dec_time}")
                
    #computing the mse for the image
    #mse=np.mean((path.astype("float")-output_path.astype("float"))**2)
    original_image=cv2.imread(path)
    stego_image=cv2.imread(output_path)
    
    
    mse_error=np.mean((original_image.astype("float")-stego_image.astype("float"))**2)          
    error_m=float(original_image.shape[0] * original_image.shape[1])
    
    print("this is mse_error value : " , mse_error)
    
    
    #computing PSNR for the images
    max_pixel_value=np.max(original_image)
    psnr=10*np.log10((max_pixel_value**2)/mse_error)
    print("this is psnr value :" , psnr)           
    
    #computing histogram for images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(original_image.ravel(), bins=256, range=(0, 256))
    plt.title('Histogram of Original Image')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 2, 2)
    plt.hist(stego_image.ravel(), bins=256, range=(0, 256))
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
    b, g, r = cv2.split(stego_image)
    
    # Calculate and plot the histograms of the red, green, and blue channels separately
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.hist(r.ravel(), bins=256, range=(0, 256), color='r')
    plt.title('stego of Red Channel')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 3, 2)
    plt.hist(g.ravel(), bins=256, range=(0, 256), color='g')
    plt.title('stego of Green Channel')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.subplot(1, 3, 3)
    plt.hist(b.ravel(), bins=256, range=(0, 256), color='b')
    plt.title('stego of Blue Channel ')
    plt.xlabel('Pixel Values')
    plt.ylabel('Frequency')
    plt.show()
    stego_entropy = information_entropy(output_path)
    print('Stego image information entropy:', stego_entropy)

    


if __name__ == '__main__':
    main()
