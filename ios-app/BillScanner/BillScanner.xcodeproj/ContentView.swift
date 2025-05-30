import SwiftUI
import UIKit

struct ContentView: View {
    @StateObject private var viewModel = ScannerViewModel()
    @State private var showImagePicker = false
    @State private var showCameraPicker = false
    @State private var sourceType: UIImagePickerController.SourceType = .camera
    
    var body: some View {
        NavigationView {
            VStack {
                if let image = viewModel.selectedImage {
                    Image(uiImage: image)
                        .resizable()
                        .scaledToFit()
                        .padding()
                }
                
                HStack {
                    Button(action: {
                        sourceType = .camera
                        showCameraPicker = true
                    }) {
                        Label("Take Photo", systemImage: "camera")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    
                    Button(action: {
                        sourceType = .photoLibrary
                        showImagePicker = true
                    }) {
                        Label("Upload", systemImage: "photo")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
                
                if viewModel.isUploading {
                    ProgressView()
                } else if let uploadedURL = viewModel.uploadedFileURL {
                    Text("Uploaded successfully!")
                    Text(uploadedURL)
                        .font(.caption)
                }
            }
            .navigationTitle("Bill Scanner")
            .sheet(isPresented: $showCameraPicker) {
                ImagePicker(selectedImage: $viewModel.selectedImage, sourceType: sourceType)
            }
            .sheet(isPresented: $showImagePicker) {
                ImagePicker(selectedImage: $viewModel.selectedImage, sourceType: sourceType)
            }
        }
    }
}
