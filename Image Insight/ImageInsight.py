import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageStat, ImageOps
from transformers import (
    BlipProcessor, BlipForConditionalGeneration,
    CLIPProcessor, CLIPModel
)

# Load BLIP model (image captioning)
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load CLIP model (style classification)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

# Style labels for classification
style_keywords = [
    "realism", "impressionism", "abstract", "surrealism", "minimalism",
    "cartoon", "anime", "pixel art", "comic style"
]

# Caption generation with BLIP
def generate_caption(image):
    inputs = blip_processor(images=image, return_tensors="pt")
    output = blip_model.generate(**inputs)
    return blip_processor.decode(output[0], skip_special_tokens=True)

# Style classification using CLIP
def classify_clip(image, labels, top_k=3):
    inputs = clip_processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)[0]
    top_indices = probs.topk(top_k).indices.tolist()
    return [(labels[i], round(probs[i].item() * 100)) for i in top_indices]

# Detect if image is mostly text (low entropy)
def is_probably_text_image(image):
    grayscale = image.convert("L")
    entropy = grayscale.entropy()
    return entropy < 4

# Get image resolution, DPI, and aspect ratio
def get_image_info(image):
    width, height = image.size
    dpi = image.info.get("dpi", (72, 72))  # Default if not set
    aspect_ratio = round(width / height, 2) if height != 0 else 0
    return width, height, dpi, aspect_ratio

# Handle image selection and analysis
def select_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not path:
        return

    image = Image.open(path).convert("RGB")

    # Add a simple border for presentation
    image_with_border = ImageOps.expand(image, border=3, fill="black")

    image_resized = image_with_border.resize((500, 375))
    photo = ImageTk.PhotoImage(image_resized)

    image_label.config(image=photo)
    image_label.image = photo

    # Get image details
    width, height, dpi, aspect_ratio = get_image_info(image)
    size_label.config(text=f"📐 Size: {width}×{height} px  |  DPI: {dpi[0]}×{dpi[1]}  |  Aspect Ratio: {aspect_ratio}")

    if is_probably_text_image(image):
        caption = "🧾 This looks like a text document."
        style = "Text Style"
    else:
        caption = generate_caption(image)
        style_results = classify_clip(image, style_keywords, top_k=3)
        style = ", ".join([label for label, _ in style_results])

    caption_label.config(text=f"📖 Caption: {caption}")
    style_label.config(text=f"🎨 Style: {style}")
    root.update_idletasks()

# Build the GUI
root = tk.Tk()
root.title("AI Image Analyzer")
root.geometry("700x640")

# Image selection button
select_btn = tk.Button(root, text="📤 Select Image", font=("Arial", 14), command=select_image)
select_btn.pack(pady=10)

# Image preview
image_label = tk.Label(root)
image_label.pack()

# Caption and style results
caption_label = tk.Label(root, text="", font=("Arial", 13), wraplength=650, justify="left")
caption_label.pack(pady=10)

style_label = tk.Label(root, text="", font=("Arial", 13))
style_label.pack(pady=5)

# New: size and DPI display
size_label = tk.Label(root, text="", font=("Arial", 13))
size_label.pack(pady=5)

# Start the app
root.mainloop()
