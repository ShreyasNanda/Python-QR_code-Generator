import io
import tkinter as tk
from tkinter import messagebox, ttk
import urllib.parse
import urllib.request
from PIL import Image, ImageTk  # Requires pillow: pip install pillow


class QRCodeApp:

  def __init__(self, root):
    self.root = root
    self.root.title("QR Code Generator")
    self.root.geometry("420x550")
    self.root.resizable(False, False)

    # Use modern styling if available
    self.style = ttk.Style()
    self.style.theme_use("clam")

    self.create_widgets()

  def create_widgets(self):
    # Main Container Frame
    main_frame = ttk.Frame(self.root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title Label
    title_label = ttk.Label(
        main_frame, text="QR Code Generator", font=("Arial", 16, "bold")
    )
    title_label.pack(pady=(0, 15))

    # Input Section Frame
    input_frame = ttk.LabelFrame(
        main_frame, text=" Enter Text or URL ", padding=15
    )
    input_frame.pack(fill=tk.X, pady=(0, 15))

    self.entry_var = tk.StringVar(value="https://www.example.com")
    self.entry = ttk.Entry(
        input_frame, textvariable=self.entry_var, font=("Arial", 11)
    )
    self.entry.pack(fill=tk.X, ipady=4, pady=(0, 10))
    self.entry.bind("<Return>", lambda event: self.generate_qr())

    # Generate Button
    self.generate_btn = ttk.Button(
        input_frame, text="Generate QR Code", command=self.generate_qr
    )
    self.generate_btn.pack(fill=tk.X, ipady=3)

    # Display Screen Frame (for the QR image)
    self.display_frame = ttk.LabelFrame(
        main_frame, text=" QR Code Preview ", padding=15
    )
    self.display_frame.pack(fill=tk.BOTH, expand=True)

    # Canvas or Label to hold the image
    self.img_label = ttk.Label(
        self.display_frame,
        text="Your QR code will appear here",
        anchor="center",
        justify="center",
    )
    self.img_label.pack(fill=tk.BOTH, expand=True)

  def generate_qr(self):
    text_data = self.entry_var.get().strip()
    if not text_data:
      messagebox.showwarning(
          "Input Error", "Please enter some text or a URL to encode."
      )
      return

    # Disable button temporarily and update text
    self.generate_btn.config(state=tk.DISABLED, text="Generating...")
    self.root.update_idletasks()

    try:
      # Encode data safely and build API request URL
      url_encoded_data = urllib.parse.quote(text_data)
      qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={url_encoded_data}"

      # Fetch image bytes directly from the URL (no file saved to disk)
      with urllib.request.urlopen(qr_api_url) as response:
        image_bytes = response.read()

      # Open image using Pillow from memory bytes
      image_stream = io.BytesIO(image_bytes)
      pil_image = Image.open(image_stream)

      # Convert to Tkinter-compatible PhotoImage
      self.qr_photo = ImageTk.PhotoImage(pil_image)

      # Update display label with the image
      self.img_label.config(image=self.qr_photo, text="")

    except Exception as e:
      messagebox.showerror(
          "Connection Error",
          f"Failed to fetch QR code.\nCheck your internet connection.\n\nDetails: {e}",
      )
    finally:
      # Reset button state
      self.generate_btn.config(state=tk.NORMAL, text="Generate QR Code")


if __name__ == "__main__":
  root = tk.Tk()
  app = QRCodeApp(root)
  root.mainloop()