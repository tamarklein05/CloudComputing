# models/firebase_init.py
import os
import firebase_admin
from firebase_admin import credentials, firestore

# נתיב לקובץ ה-Service Account שלך
SERVICE_ACCOUNT = os.environ.get('FIREBASE_SERVICE_ACCOUNT', './infra/firebase-service-account.json')

# אתחול אפליקציית Firebase (רק פעם אחת)
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)

# חיבור למסד הנתונים Firestore
db = firestore.client()

def upload_to_firebase(data: dict):
    """
    שומר נתונים במסד Firestore תחת collection בשם 'uploads'
    """
    try:
        doc_ref = db.collection('uploads').add(data)
        return {"id": doc_ref[1].id}
    except Exception as e:
        return {"error": str(e)}
