import tkinter as tk
from tkinter import filedialog
from main import VideoProcessor

class LicensePlateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("License Plate Detection GUI")

        self.camera_var = tk.StringVar()
        self.camera_var.set("Select Camera")
        self.camera_label = tk.Label(root, text="Select Source:")
        self.camera_label.pack()

        self.camera_dropdown = tk.OptionMenu(root, self.camera_var, "Select Camera", "Camera 1", "Camera 2")
        self.camera_dropdown.pack()

        self.video_label = tk.Label(root, text="Video Path:")
        self.video_label.pack()

        self.video_button = tk.Button(root, text="Browse", command=self.browse_video)
        self.video_button.pack()

        self.model_label = tk.Label(root, text="Select Model:")
        self.model_label.pack()

        self.model_button = tk.Button(root, text="Browse", command=self.browse_model)
        self.model_button.pack()

        self.process_button = tk.Button(root, text="Process Video", command=self.process_video)
        self.process_button.pack()
    def open_csv(self):
        csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if csv_file_path:
            try:
                # Check if the file exists before opening it
                if os.path.exists(csv_file_path):
                    os.system("start excel " + csv_file_path)  # Open the CSV file with Excel (Windows)
                    # If you're on a different platform, you might need to use a different command to open the CSV
                else:
                    print(f"File not found: {csv_file_path}")
            except Exception as e:
                print(f"Error opening CSV: {e}")
    def browse_video(self):
        if self.camera_var.get() == "Camera 1":
            self.video_path = "0"
        elif self.camera_var.get() == "Camera 2":
            self.video_path = "1"
        else:
            video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
            if video_path:
                self.video_path = video_path

    def browse_model(self):
        model_path = filedialog.askopenfilename(filetypes=[("Model Files", "*.pt")])
        if model_path:
            self.model_path = model_path

    def process_video(self):
        if hasattr(self, 'video_path') and hasattr(self, 'model_path'):
            video_processor = VideoProcessor(self.video_path, self.model_path)
            video_processor.process_video()
            video_path = "C:\\Users\shitosu\Desktop\Tkm_front.mp4"
            model_path = "C:\\Users\\shitosu\\Desktop\\v8\\best.pt"

            video_processor = VideoProcessor(video_path, model_path)
            video_processor.process_video()

        else:
            print("Please select both video source and model.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LicensePlateGUI(root)
    root.mainloop()
