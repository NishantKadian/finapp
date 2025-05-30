import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import io
from datetime import datetime
from google.cloud import storage
import os
from dotenv import load_dotenv

class BillScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Scanner")
        self.root.geometry("800x600")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('vista')
        
        # Main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview area
        self.preview_label = ttk.Label(self.main_frame)
        self.preview_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Buttons
        ttk.Button(self.main_frame, text="Take Photo", command=self.capture_photo).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.main_frame, text="Upload File", command=self.upload_file).grid(row=1, column=1, padx=5, pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Initialize camera
        self.camera = None
        self.preview_image = None
        
    def capture_photo(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            
        ret, frame = self.camera.read()
        if ret:
            # Convert to RGB for PIL
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            
            # Resize to fit preview
            image.thumbnail((640, 480))
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
            
            # Store the image for upload
            self.preview_image = image
            
            # Add upload button
            ttk.Button(self.main_frame, text="Save to Cloud", 
                      command=self.upload_captured).grid(row=3, column=0, columnspan=2, pady=5)
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.pdf")]
        )
        if file_path:
            with open(file_path, 'rb') as f:
                self.upload_to_gcs(f.read())
    
    def upload_captured(self):
        if self.preview_image:
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            self.preview_image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            self.upload_to_gcs(img_byte_arr)
    
    def upload_to_gcs(self, image_bytes, bucket_name="finapp_nk"):
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
            
            gcs_uri = f"gs://{bucket_name}/{blob_name}"
            self.status_label.configure(
                text=f"Upload successful!\nStored at: {gcs_uri}",
                foreground="green"
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Error uploading: {str(e)}",
                foreground="red"
            )
    
    def cleanup(self):
        if self.camera is not None:
            self.camera.release()

if __name__ == "__main__":
    load_dotenv()
    root = tk.Tk()
    app = BillScannerApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cleanup(), root.destroy()))
    root.mainloop()
