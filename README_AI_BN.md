# NIRVOY BOT AI CONTROL — FIXED v4

## এই ভার্সনে কী ঠিক হয়েছে
আগের সমস্যায় সাধারণ প্রশ্ন যেমন `Hello` / `কেমন আছেন`-কেও configuration JSON হিসেবে parse করা হচ্ছিল। ফলে Gemini স্বাভাবিক উত্তর দিলেও bot সেটাকে ভুল format বলে দেখাত।

v4-এ:
- সাধারণ chat → সরাসরি normal text response
- configuration request → allow-listed JSON/action mode
- JSON mode-এ Gemini `responseMimeType=application/json` ব্যবহার করা হয়
- configuration change এখনো confirmation ছাড়া apply হয় না
- AI arbitrary Python/shell/SQL execute করতে পারে না

## Setup
`.env`-এ নিজের নতুন credentials বসান:

```env
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_OWNER_ID
GEMINI_API_KEY=YOUR_NEW_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
GEMINI_AUTO_MODEL=true
```

তারপর:

```bash
pip install -r requirements.txt
python main.py
```

Telegram:
- `/ai` → AI chat
- `/aistatus` → Gemini status

## Test
AI chat-এ পাঠান:
- `Hello`
- `কেমন আছেন?`
- `প্রমোশন detection কেন কাজ করে?`

তারপর configuration test:
- `anti-promo চালু করো`
- `বর্তমান settings দেখাও`

Configuration change-এর ক্ষেত্রে bot আগে confirmation চাইবে।


## 🔊 লিংক/প্রমোশন সতর্কবার্তা ভয়েস

- অ্যাডমিন ড্যাশবোর্ডে `🔊 সতর্কবার্তা ভয়েস সেটিংস` খুলুন।
- বটের ব্যক্তিগত ইনবক্সে Telegram Voice Message অথবা ফোন থেকে audio file/document পাঠান। শুধু OWNER_ID বা সক্রিয় admin session-এর আপলোড সংরক্ষণ হবে।
- একাধিক ভয়েস যোগ করা যায়। একই সদস্যের জন্য একই গ্রুপে একটি ভয়েস নির্ধারিত থাকবে; নতুন সদস্যদের ভয়েস এলোমেলোভাবে বেছে নেওয়া হবে।
- সেটিংসের `মুছুন` বাটন দিয়ে ভয়েস সরিয়ে নতুন ভয়েস যোগ করা যাবে।
- লিংক/প্রমোশন শনাক্ত হলে মূল মেসেজ ডিলিট হবে এবং কোনো টেক্সট সতর্কবার্তা ছাড়া ভয়েস পাঠানোর চেষ্টা হবে। সদস্য বটকে `/start` না দিয়ে থাকলে ব্যক্তিগত DM ব্যর্থ হতে পারে; তখন ভয়েস গ্রুপে পাঠানো হবে। পাঠানো ভয়েস ৫ মিনিট পরে মুছে ফেলার চেষ্টা হবে।
- গ্রুপে ভয়েস পাঠানোর জন্য বটকে প্রয়োজনীয় গ্রুপ অনুমতি দিতে হবে।
