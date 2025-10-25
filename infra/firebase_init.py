# firebase_init.py
import os
import firebase_admin
from firebase_admin import credentials, firestore

# נתיב ל־service account JSON
SERVICE_ACCOUNT = os.environ.get('FIREBASE_SERVICE_ACCOUNT', './infra/firebase-service-account.json')

# טוען את ה־service account ומאתחל את האפליקציה של Firebase
cred = credentials.Certificate(SERVICE_ACCOUNT)
firebase_admin.initialize_app(cred)

# לקוח Firestore לשימוש באפליקציה
db = firestore.client()
