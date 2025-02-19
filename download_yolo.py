from ultralytics import YOLO

def download_model():
    print("Downloading YOLOv8 model...")
    model = YOLO('yolov8n.pt')
    print("Model downloaded successfully!")

if __name__ == "__main__":
    download_model() 