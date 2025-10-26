# models/cloudinary_helpers.py
import os
import cloudinary
import cloudinary.uploader

# הגדרות Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

def upload_to_cloudinary(file):
    """
    מעלה קובץ ל-Cloudinary ומחזיר את ה-URL של התמונה
    """
    try:
        result = cloudinary.uploader.upload(file)
        return result.get("secure_url")
    except Exception as e:
        return {"error": str(e)}
