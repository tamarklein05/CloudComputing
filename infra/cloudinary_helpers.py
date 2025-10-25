import os
import urllib.parse

CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
API_KEY = os.environ.get('CLOUDINARY_API_KEY')
API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

def build_image_url(query):
    """
    בנייה פשוטה של URL תמונה ב־Cloudinary על בסיס query.
    בגרסה בסיסית זו אנו מניחים שניתן למצוא משאב שכבר קיים בשם ה'query'.
    """
    if not CLOUD_NAME:
        raise RuntimeError("CLOUDINARY_CLOUD_NAME is not set")
    encoded = urllib.parse.quote_plus(query)
    return f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/q_auto,f_auto/{encoded}.jpg"
