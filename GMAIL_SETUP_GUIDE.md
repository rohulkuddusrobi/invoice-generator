# Gmail App Password Setup Guide

## 🚨 সমস্যা: Gmail Authentication Failed

আপনার current password "NotFound#404" Gmail দ্বারা accept হচ্ছে না।
Gmail এ email পাঠানোর জন্য **App Password** প্রয়োজন।

## ✅ সমাধান:

### 1. 2-Factor Authentication Enable করুন:
- যান: https://myaccount.google.com
- Security > 2-Step Verification
- Turn On করুন

### 2. App Password তৈরি করুন:
- যান: https://myaccount.google.com/apppasswords
- Select app: Mail
- Generate ক্লিক করুন
- 16-character password copy করুন

### 3. নতুন password দিয়ে test করুন:
```python
python test_gmail_setup.py
```

## 📱 Example App Password:
```
Old password: NotFound#404
New App Password: abcd efgh ijkl mnop (example)
```

## 🔄 App Password পাওয়ার পর:
1. নতুন password দিয়ে email_config.json update করুন
2. অথবা আমাকে নতুন App Password দিন, আমি update করে দেব

## 📞 Need Help?
App Password generate করতে সমস্যা হলে আমাকে বলুন!
