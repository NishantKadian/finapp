import SwiftUI
import GoogleCloudStorage

class ScannerViewModel: ObservableObject {
    @Published var selectedImage: UIImage?
    @Published var isUploading = false
    @Published var uploadedFileURL: String?
    
    func uploadImage(_ image: UIImage) {
        isUploading = true
        
        // Configure GCS client
        let storage = Storage.storage()
        let storageRef = storage.reference()
        
        // Create file name with timestamp
        let timestamp = Int(Date().timeIntervalSince1970)
        let imagePath = "data/captured_image_\(timestamp).jpg"
        let imageRef = storageRef.child(imagePath)
        
        // Convert image to data
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            return
        }
        
        // Upload to GCS
        let metadata = StorageMetadata()
        metadata.contentType = "image/jpeg"
        
        imageRef.putData(imageData, metadata: metadata) { metadata, error in
            DispatchQueue.main.async {
                self.isUploading = false
                
                if let error = error {
                    print("Error uploading: \(error.localizedDescription)")
                    return
                }
                
                // Get the download URL
                imageRef.downloadURL { url, error in
                    if let downloadURL = url?.absoluteString {
                        self.uploadedFileURL = downloadURL
                    }
                }
            }
        }
    }
}
