# Major_Project_ExploringAdvancedEncryptionandSteganographyTechniquesforImageSecurity_Mohak_kataria
## Author: MOHAK KATARIA (AMENP2CSN21014)

This project implements steganography techniques to hide encrypted messages within images using two different methods: Least Significant Bit (**LSB**) and **Spread Spectrum**.

---
# Table of Contents
1. [Description](#Description)
2. [Features](#Features)
3. [Installation](#Installation)
4. [Usage](#Usage)

## Description
Steganography is the practice of concealing information within other non-secret data, such as images. This project utilizes steganography to hide encrypted messages within images using two different approaches: Least Significant Bit (**LSB**) and **Spread Spectrum**.

The **LSB** method replaces the least significant bits of the image pixels with the bits of the encrypted message, making minimal visual changes to the image. On the other hand, **Spread Spectrum** embeds the encrypted message by spreading it across multiple image pixels, resulting in a more robust and imperceptible hiding technique.


## Features
1. Support for multiple encryption algorithms: **AES, DES, ChaCha20**, and **RSA**.
2. Embedding encrypted messages within image files using the **LSB** method.
3. Extracting encrypted messages from steganographic images using the **LSB** method.
4. Embedding encrypted messages within image files using the **Spread Spectrum** method.
5. Extracting encrypted messages from steganographic images using the **Spread Spectrum** method.

## Installation
1. Clone the repository:
    
    `git clone https://github.com/AmritaCSN/Major_Project_ExploringAdvancedEncryptionandSteganographyTechniquesforImageSecurity_Mohak_kataria.git`

2. Navigate to the project directory:
    
    `cd Major_Project_ExploringAdvancedEncryptionandSteganographyTechniquesforImageSecurity_Mohak_kataria`

3. Install the required dependencies:
    
    `pip install -r requirements.txt`

## Usage
Run the **LSB** embedding and image extraction: `python lsb.py`

Follow the prompts to select the encryption algorithm, provide the necessary inputs (image file), and specify the output filenames.

The program will encrypt the _plaintext_, embed the encrypted message within the image using **LSB**, and save the steganographic image.

Run the **Spread Spectrum** embedding and extraction: `python ss.py`

Follow the prompts to select the encryption algorithm, provide the necessary inputs (_plaintext, key, image file_), and specify the output filenames.

The program will encrypt the _plaintext_, embed the encrypted message within the image using **Spread Spectrum**, and save the steganographic image.

To extract the encrypted message from the steganographic image, run the **Spread Spectrum** extraction again and provide the steganographic image file.
