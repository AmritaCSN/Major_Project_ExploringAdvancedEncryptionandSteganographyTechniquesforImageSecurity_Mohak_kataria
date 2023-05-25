# Major_Project_ExploringAdvancedEncryptionandSteganographyTechniquesforImageSecurity_Mohak_kataria


This project implements steganography techniques to hide encrypted messages within images using two different methods: Least Significant Bit (LSB) and Spread Spectrum.
Table of Contents

    Description
    Features
    Installation
    Usage

Description

Steganography is the practice of concealing information within other non-secret data, such as images. This project utilizes steganography to hide encrypted messages within images using two different approaches: Least Significant Bit (LSB) and Spread Spectrum.

The LSB method replaces the least significant bits of the image pixels with the bits of the encrypted message, making minimal visual changes to the image. On the other hand, Spread Spectrum embeds the encrypted message by spreading it across multiple image pixels, resulting in a more robust and imperceptible hiding technique.
Features

    Support for multiple encryption algorithms: AES, DES, ChaCha20, and RSA.
    Embedding encrypted messages within image files using the LSB method.
    Extracting encrypted messages from steganographic images using the LSB method.
    Embedding encrypted messages within image files using the Spread Spectrum method.
    Extracting encrypted messages from steganographic images using the Spread Spectrum method.

Installation

    Clone the repository: git clone https://github.com/your-username/steganography.git

Navigate to the project directory:

cd steganography

Install the required dependencies:

    pip install -r requirements.txt

Usage

    Run the LSB embedding and extraction: python lsb.py


Follow the prompts to select the encryption algorithm, provide the necessary inputs (image file), and specify the output filenames.

The program will encrypt the plaintext, embed the encrypted message within the image using LSB, and save the steganographic image.
To extract the encrypted message from the steganographic image, run the LSB extraction again and provide the steganographic image file.

    Run the Spread Spectrum embedding and extraction: python spread_spectrum.py

Follow the prompts to select the encryption algorithm, provide the necessary inputs (plaintext, key, image file), and specify the output filenames.

The program will encrypt the plaintext, embed the encrypted message within the image using Spread Spectrum, and save the steganographic image.

To extract the encrypted message from the steganographic image, run the Spread Spectrum extraction again and provide the steganographic image file.
