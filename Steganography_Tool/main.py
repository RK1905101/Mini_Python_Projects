import streamlit as st
from PIL import Image
import io

# ----------------------------------------------------
# 🧠 Function: Encode (Hide Text in Image)
# ----------------------------------------------------
def encode_image(image, secret_text):
    img = image.convert("RGB")
    encoded = img.copy()
    width, height = img.size
    index = 0

    # Convert message to binary and add a special delimiter
    binary_secret = ''.join(format(ord(i), '08b') for i in secret_text) + '1111111111111110'

    for row in range(height):
        for col in range(width):
            if index < len(binary_secret):
                r, g, b = img.getpixel((col, row))
                r = (r & ~1) | int(binary_secret[index])
                encoded.putpixel((col, row), (r, g, b))
                index += 1
            else:
                break
        if index >= len(binary_secret):
            break

    return encoded


# ----------------------------------------------------
# 🕵️ Function: Decode (Extract Hidden Text)
# ----------------------------------------------------
def decode_image(image):
    img = image.convert("RGB")
    binary_data = ''
    for row in range(img.height):
        for col in range(img.width):
            r, g, b = img.getpixel((col, row))
            binary_data += str(r & 1)

    # Split the binary data into 8-bit chunks
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_text = ''
    for byte in all_bytes:
        char = chr(int(byte, 2))
        decoded_text += char
        if decoded_text.endswith("þ"):  # stop at delimiter
            return decoded_text[:-1]  # remove delimiter
    return ""


# ----------------------------------------------------
# 🎨 STREAMLIT UI
# ----------------------------------------------------
st.set_page_config(page_title="🔐 Steganography Tool", page_icon="🖼️", layout="centered")

st.title("🔐 Image Steganography Tool")
st.write("Easily hide secret messages inside images or extract them securely using Python 🧠")

mode = st.radio("Choose an option:", ["📝 Encode Message", "🔍 Decode Message"])

# ---------------- Encode Mode ----------------
if mode == "📝 Encode Message":
    uploaded_image = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    secret_message = st.text_area("Enter the secret message you want to hide:")

    if uploaded_image and secret_message:
        if st.button("Encode 🔒"):
            image = Image.open(uploaded_image)
            encoded_img = encode_image(image, secret_message + "þ")  # add delimiter explicitly

            # Convert to BytesIO for download
            img_bytes = io.BytesIO()
            encoded_img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            st.image(encoded_img, caption="✅ Encoded Image Preview", use_container_width=True)
            st.download_button(
                label="⬇️ Download Encoded Image",
                data=img_bytes,
                file_name="encoded_image.png",
                mime="image/png"
            )
            st.success("Message successfully encoded inside the image!")

# ---------------- Decode Mode ----------------
elif mode == "🔍 Decode Message":
    uploaded_encoded_image = st.file_uploader("Upload an encoded image (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if uploaded_encoded_image:
        if st.button("Decode 🕵️"):
            image = Image.open(uploaded_encoded_image)
            hidden_message = decode_image(image)
            if hidden_message:
                st.success("✅ Hidden message found!")
                st.text_area("🔓 Decoded Message:", hidden_message, height=100)
            else:
                st.error("⚠️ No hidden message found or image not encoded properly.")

st.markdown("---")
st.caption("Made with ❤️ using Python & Streamlit")
