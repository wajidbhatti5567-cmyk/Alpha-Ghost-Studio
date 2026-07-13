from PIL import Image, ImageDraw, ImageFont
import os

class ThumbnailEngine:
    def __init__(self):
        self.output_dir = "thumbnails"
        os.makedirs(self.output_dir, exist_ok=True)
        # Font setting (make sure to have a .ttf file in assets)
        self.font_path = "assets/fonts/impact.ttf" 

    def create_pro_thumbnail(self, title, episode, brand="Alpha Ghost Studio"):
        """Generates a high-level thumbnail autonomously."""
        print(f"Creating thumbnail for: {title}")
        
        # 1. Create a base canvas (YouTube Standard 16:9)
        img = Image.new('RGB', (1920, 1080), color=(255, 69, 0)) # YouTube Red/Orange theme
        draw = ImageDraw.Draw(img)
        
        # 2. Add Brand Name (Top)
        font_brand = ImageFont.truetype(self.font_path, 60)
        draw.text((50, 50), brand, fill=(255, 255, 255), font=font_brand)
        
        # 3. Add Episode Number (Big and Bold)
        font_ep = ImageFont.truetype(self.font_path, 150)
        draw.text((50, 150), f"EPISODE {episode}", fill=(255, 255, 255), font=font_ep)
        
        # 4. Add Roman Urdu/English Title
        # Title example: "Mota aur Patlu ki funny larayi"
        font_title = ImageFont.truetype(self.font_path, 100)
        draw.text((50, 400), title, fill=(255, 255, 0), font=font_title)
        
        # 5. Save the file
        thumb_path = os.path.join(self.output_dir, f"thumb_ep_{episode}.png")
        img.save(thumb_path)
        
        return thumb_path
