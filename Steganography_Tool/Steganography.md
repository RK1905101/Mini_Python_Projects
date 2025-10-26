🖼️ Image Steganography Tool
🔐 Hide Secret Messages Inside Images — Securely and Simply

This project lets you encode (hide) secret text messages inside ordinary images and later decode (extract) them back using Python and Streamlit.
It demonstrates the concept of Steganography, which is the practice of concealing information within non-suspicious files — an important concept in cybersecurity and digital forensics.

⚙️ How It Works

Each image pixel contains 3 color values (Red, Green, Blue).

This tool slightly changes the least significant bit (LSB) of the red channel in each pixel to store bits of your secret message.

The change is invisible to the human eye, so the image looks exactly the same.

When decoding, the program reads those bits and reconstructs the original hidden message.

🧰 Tech Stack

Python 3

Streamlit — for a simple web UI

Pillow (PIL) — for image processing