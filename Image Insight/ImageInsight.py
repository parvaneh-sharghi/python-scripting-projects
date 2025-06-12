import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel

# Load models once
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

# Keywords
style_keywords = ["realism", "impressionism", "abstract", "surrealism", "minimalism", "cartoon", "anime", "pixel art", "comic style"]
emotion_keywords = [ "joyful", "sad", "angry", "peaceful", "romantic", "nostalgic", "hopeful",
    "fearful", "lonely", "confused", "excited", "melancholy", "serene", "anxious",
    "playful", "depressed", "curious", "grateful", "ashamed", "surprised",
    "inspired", "gloomy", "tender", "tense", "bored", "empathetic", "jealous"]

# Caption generator
def generate_caption(image):
    inputs = blip_processor(images=image, return_tensors="pt")
    output = blip_model.generate(**inputs)
    return blip_processor.decode(output[0], skip_special_tokens=True)

# CLIP classification
def classify_clip(image, labels):
    inputs = clip_processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)
    best_idx = probs.argmax().item()
    return labels[best_idx]

# Handle image selection
def select_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not path:
        return

    image = Image.open(path).convert("RGB")
    image_resized = image.resize((500, 375))
    photo = ImageTk.PhotoImage(image_resized)

    image_label.config(image=photo)
    image_label.image = photo

    caption = generate_caption(image)
    style = classify_clip(image, style_keywords)
    emotion = classify_clip(image, emotion_keywords)

    caption_label.config(text=f"📖 Caption: {caption}")
    style_label.config(text=f"🎨 Style: {style}")
    emotion_label.config(text=f"😄 Emotion: {emotion}")

# Setup GUI
root = tk.Tk()
root.title("AI Image Analyzer")
root.geometry("700x600")  # Increased window size

select_btn = tk.Button(root, text="📤 Select Image", font=("Arial", 14), command=select_image)
select_btn.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

caption_label = tk.Label(root, text="", font=("Arial", 13), wraplength=650, justify="left")
caption_label.pack(pady=10)

style_label = tk.Label(root, text="", font=("Arial", 13))
style_label.pack(pady=5)

emotion_label = tk.Label(root, text="", font=("Arial", 13))
emotion_label.pack(pady=5)

root.mainloop()
