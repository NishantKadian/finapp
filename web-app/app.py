import streamlit as st
from google.cloud import storage
import os
from PIL import Image
import io
from datetime import datetime

# Setup page config to make it look more like a mobile app
st.set_page_config(
    page_title="Bill Scanner",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for iOS-like appearance
st.markdown("""
    <style>
    .stApp {
        max-width: 414px;
        margin: 0 auto;
        background-color: #f2f2f7;
        padding: 10px;
    }
    .css-1d391kg {
        padding: 1rem 1rem;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #007AFF;
        color: white;
        border: none;
        padding: 10px 20px;
        width: 100%;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

def upload_to_gcs(image_bytes, bucket_name="finapp_nk"):
    """Upload image to Google Cloud Storage"""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"data/captured_image_{timestamp}.jpg"
        blob = bucket.blob(blob_name)
        
        blob.upload_from_string(
            image_bytes,
            content_type="image/jpeg"
        )
        return f"gs://{bucket_name}/{blob_name}"
    except Exception as e:
        st.error(f"Error uploading to GCS: {str(e)}")
        return None

def main():
    st.title("📷 Bill Scanner")
    
    # Camera input
    camera_tab, upload_tab = st.tabs(["Take Photo", "Upload Image"])
    
    with camera_tab:
        camera_image = st.camera_input("Take a picture")
        
        if camera_image:
            # Display the captured image
            st.image(camera_image)
            
            if st.button("Save to Cloud"):
                # Convert the image to bytes and upload
                img_bytes = camera_image.getvalue()
                gcs_uri = upload_to_gcs(img_bytes)
                
                if gcs_uri:
                    st.success("Image uploaded successfully!")
                    st.write(f"Stored at: {gcs_uri}")
    
    with upload_tab:
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "pdf"])
        
        if uploaded_file:
            # Display the uploaded image
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file)
            
            if st.button("Upload to Cloud"):
                gcs_uri = upload_to_gcs(uploaded_file.getvalue())
                
                if gcs_uri:
                    st.success("File uploaded successfully!")
                    st.write(f"Stored at: {gcs_uri}")

if __name__ == "__main__":
    main()
