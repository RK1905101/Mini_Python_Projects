import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="AI Background Remover", page_icon="🖼️", layout="centered")
st.title("🖼️ AI Background Remover")

uploaded_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    
    # Display original image
    img = Image.open(uploaded_file)
    st.subheader("Original Image")
    st.image(img, use_container_width=True)

    if st.button("Remove Background"):
        with st.spinner("Processing... Please wait"):

            uploaded_file.seek(0)  # ✅ Reset pointer before second read
            input_image = uploaded_file.read()

            output = remove(input_image)
            result_image = Image.open(io.BytesIO(output))

        st.success("✅ Background Removed Successfully!")
        st.subheader("Output Image")
        st.image(result_image, use_container_width=True)

        # Download button
        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        byte_data = buf.getvalue()

        st.download_button(
            label="📥 Download Output",
            data=byte_data,
            file_name="removed_bg.png",
            mime="image/png"
        )
