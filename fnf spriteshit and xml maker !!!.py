from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import Image
import xml.etree.ElementTree as ET
import os

# Global variables
directions = ["idle", "up", "down", "right", "left"]
image_paths = {}
frame_counts = 4

# Function to handle image selection for a specific direction and frame
def select_image(direction, frame):
    filename = askopenfilename(filetypes=[("Image Files", "*.png")])
    if filename:
        if direction not in image_paths:
            image_paths[direction] = {}

        image_paths[direction][frame] = filename
        print(f"Selected image for {direction} - Frame {frame}: {filename}")
    else:
        print(f"No image selected for {direction} - Frame {frame}.")

# Function to generate the spritesheet
def generate_spritesheet():
    if all(direction in image_paths and len(image_paths[direction]) == frame_counts for direction in directions):
        max_width = 0
        total_height = 0
        subtextures = []

        for direction in directions:
            images = [Image.open(filename) for filename in image_paths[direction].values()]
            max_width = max(max_width, max(image.size[0] for image in images))
            total_height += sum(image.size[1] for image in images)

        spritesheet = Image.new("RGBA", (max_width, total_height))
        y_offset = 0

        for direction in directions:
            images = [Image.open(filename) for filename in image_paths[direction].values()]
            max_height = max(image.size[1] for image in images)
            x_offset = 0
            frame_number = 1

            for image in images:
                resized_image = image.resize((image.size[0] * 2, image.size[1] * 2))  # Increase sprite size
                spritesheet.paste(resized_image, (x_offset, y_offset))
                subtexture = {
                    "name": f"char_{direction}{frame_number:04d}",
                    "x": str(x_offset),
                    "y": str(y_offset),
                    "width": str(resized_image.size[0]),  # Use resized image size
                    "height": str(resized_image.size[1]),  # Use resized image size
                    "frameX": "0",
                    "frameY": "0",
                    "frameWidth": str(resized_image.size[0]),  # Use resized image size
                    "frameHeight": str(resized_image.size[1])  # Use resized image size
                }
                subtextures.append(subtexture)
                x_offset += resized_image.size[0]
                frame_number += 1

            y_offset += max_height * 2  # Increase y_offset to accommodate larger sprites

        spritesheet.save(os.path.join(os.getcwd(), "funnisheet.png"))
        generate_xml(subtextures)
        print("Spritesheet and XML generated successfully.")
    else:
        print("Please select images for all directions and frames.")

# Function to generate the XML file
def generate_xml(subtextures):
    root = ET.Element("TextureAtlas", imagePath="funnisheet.png")

    for subtexture in subtextures:
        sub = ET.SubElement(root, "SubTexture", attrib=subtexture)

    tree = ET.ElementTree(root)
    tree.write(os.path.join(os.getcwd(), "funnisheet.xml"))

# Create the Tkinter application
root = Tk()

# Create labels and buttons for image selection
for direction in directions:
    label = Label(root, text=direction)
    label.pack()

    for frame in range(1, frame_counts + 1):
        button = Button(root, text=f"Select Image - Frame {frame:02d}", command=lambda dir=direction, f=frame: select_image(dir, f))
        button.pack()

# Create the "Generate Spritesheet" button
generate_button = Button(root, text="Generate Spritesheet", command=generate_spritesheet)
generate_button.pack()

# Function to check if at least one image is selected
def check_image_selection():
    if not any(image_paths.values()):
        print("Please select at least 1 image.")

# Create the "Check Image Selection" button
check_button = Button(root, text="Check Image Selection", command=check_image_selection)
check_button.pack()

# Run the Tkinter event loop
root.mainloop()
