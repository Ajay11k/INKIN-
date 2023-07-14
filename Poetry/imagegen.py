from PIL import Image, ImageDraw, ImageFont
import os
import time

def add_text_to_image(text, theme,image_path,language):
    if language=="en":
         font = ImageFont.truetype("static/Courgette-Regular.ttf", size=50)
    else:
        font = ImageFont.truetype("static/TiroDevanagariHindi-Italic.ttf", size=60)
        
        
    # Load the image
    
    
    # Define the theme settings
    if theme == "1":
        color = (255, 195, 0)  # Magenta
        alignment = "center"
        spacing = 20
        
        
    elif theme == "2":
        color = (41,36,33)  # Green
        alignment = "center"
        spacing = 30
        
        
    elif theme == "3":
        color = (139, 0, 0)  # Blue
        alignment = "left"
        spacing = 15
        
        
    elif theme == "4":
        color = 	(0,255,127) # Yellow
        alignment = "center"
        spacing = 25
       
        
    
        # Invalid theme, use default settings
    else:
        color = (255, 0, 255)  # Magenta
        alignment = "right"
        spacing = 20
        
        
          
    image = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)
    # Set padding size
    padding = 20
    position = (0, 0)

    # Calculate the text size
    bbox = draw.multiline_textbbox(position, text, font=font, align=alignment, spacing=spacing)

    # Calculate the text width and height
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    print(text_height,text_width,image.width,image.height)
    if text_width > image.width or text_height > image.height:
        print("hiiii")
        
        # Calculate the new image size with padding
        new_width = image.width
        new_height = image.height
        
        if text_width > image.width:
            print(1)
            new_width = text_width + 10 * padding
        
        if text_height > image.height:
            print(2)
            new_height = text_height + 10 * padding
        print(new_width)
        # Calculate the aspect ratio of the original image
        aspect_ratio = image.width / image.height
        
        # Calculate the new width and height while preserving the aspect ratio
        if new_width / new_height > aspect_ratio:
            new_height = new_width / aspect_ratio
        else:
            new_width= new_height * aspect_ratio
        
        # Print the new width and height
        print("New Width:", new_width)
        print("New Height:", new_height)


        new_width=int(new_width)
        new_height=int(new_height)
        # Create a new image with the adjusted size
        resized_image = image.resize((new_width, new_height))

        # Create a new image with the resized image as the background
        new_image = Image.new("RGB", (new_width, new_height))
        new_image.paste(resized_image)

        # Update the image and drawing object
        image = new_image

        draw = ImageDraw.Draw(image)

    # Calculate the position to center the text within the image (excluding padding)
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # Draw the text on the image
    draw.multiline_text((x, y), text, font=font, fill=color, align=alignment, spacing=spacing)

    # Save the modified image
    output_path = "static/image_with_text.jpg"

    # Generate a timestamp
    timestamp = str(int(time.time()))

    # Add timestamp to the file name
    file_name = f"image_with_text_{timestamp}.jpg"

    # Create the new output path with the updated file name
    new_output_path = os.path.join("static", file_name)
   
    image.save(new_output_path)

    # Delete the previous image if it exists
    # if os.path.exists(output_path):
    #     os.remove(output_path)

    # Return the new output path
    return new_output_path

# Example usage
# image_path = r"static\Images\bg1.jpg"
# text = "तुम मेरे प्यार हो\n    तुम मेरे प्यार हो\nतुम मेरे प्यार हो\n    तुम मेरे प्यार हो"


# result_image_path = add_text_to_image( text,"1",image_path)
# print("Image with text saved at:", result_image_path)

# from PIL import Image, ImageDraw, ImageFont

# # Load the image
# image = Image.open("bg.jpg")

# # Create a drawing object
# draw = ImageDraw.Draw(image)

# # Define the text parameters
# text = "Line 1\n    Line 2\nLine 3\n    Line 4"
# font = ImageFont.truetype("arial.ttf", size=100)
# color = (255, 0, 255)  # RGB color tuple

# # Set padding size
# padding = 20
# position = (400, 400)
# alignment = "right"
# space = 20

# # Calculate the text size
# bbox = draw.multiline_textbbox(position, text, font=font, align=alignment, spacing=space)

# # Calculate the text width and height
# text_width = bbox[2] - bbox[0]
# text_height = bbox[3] - bbox[1]

# # Calculate the new image size with padding
# new_width = max(text_width, image.width) + 10 * padding
# new_height = max(text_height, image.height) + 10 * padding

# # Create a new image with the adjusted
# resized_image = image.resize((new_width, new_height))

# # Create a new image with the resized image as the background
# new_image = Image.new("RGB", (new_width, new_height))
# new_image.paste(resized_image)

# # Update the image and drawing object
# image = new_image


# # Paste the original image onto the new image

# draw = ImageDraw.Draw(image)

# # Calculate the position to center the text within the image (excluding padding)
# x = (image.width - text_width) // 2
# y = (image.height - text_height) // 2

# # Draw the text on the image
# draw.multiline_text((x, y), text, font=font, fill=color, align=alignment, spacing=space)

# # Save the modified image
# image.save("image_with_text.jpg")

