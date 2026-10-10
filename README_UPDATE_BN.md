# NIRVOY GUARD — Voice Moderation Update

## এই আপডেটে
- লিংক/প্রমোশন/স্প্যাম মেসেজ ডিলিট হলে টেক্সট সতর্কবার্তার বদলে সংরক্ষিত ভয়েস বা অডিও পাঠানোর চেষ্টা করবে।
- প্রথমে offending member-কে private message পাঠানোর চেষ্টা হবে। সে বটকে `/start` না দিয়ে থাকলে DM ব্যর্থ হতে পারে; তখন ভয়েস/অডিও গ্রুপে পাঠানো হবে।
- পাঠানো ভয়েস/অডিও ৫ মিনিট পরে মুছে ফেলার চেষ্টা হবে; বটের যথাযথ অনুমতি থাকা দরকার।
- Dashboard-এ `🔊 সতর্কবার্তা ভয়েস সেটিংস` মেনু আছে।
- বটের private inbox-এ Telegram voice message অথবা audio file/document পাঠিয়ে ভয়েস যোগ করা যাবে।
- মেনু থেকে যেকোনো সংরক্ষিত ভয়েস মুছে নতুনটি যোগ করা যাবে।
- একাধিক ভয়েস থাকলে প্রতি গ্রুপে সদস্যদের আলাদা ভয়েস বরাদ্দ দেওয়ার চেষ্টা হবে; ভয়েস কম হলে পুনরাবৃত্তি হতে পারে।

## আপডেট করার আগে
1. পুরোনো বট বন্ধ করুন।
2. পুরোনো ফোল্ডারের `.env` এবং `nirvoy_guard.db` ব্যাকআপ রাখুন।
3. ZIP Extract করুন। নিজের পুরোনো `.env` ফাইলটি নতুন ফোল্ডারে কপি করুন। পুরোনো ডেটা/সেটিংস রাখতে চাইলে `nirvoy_guard.db`-ও কপি করুন।
4. `.env` না থাকলে `.env.example` কপি করে `.env` নাম দিন, তারপর নিজের BOT_TOKEN, OWNER_ID, ADMIN_SECRET_KEY ইত্যাদি বসান।
5. `pip install -r requirements.txt` চালান এবং `python main.py` দিয়ে চালু করুন।
6. BotFather থেকে পাওয়া সঠিক bot username খুলে `/start` দিন, Dashboard-এ Voice Settings খুলুন, তারপর voice message বা audio upload করুন।

## গুরুত্বপূর্ণ
- বটকে গ্রুপে Admin করে Delete Messages অনুমতি দিন। গ্রুপে সতর্কবার্তা ভয়েস পোস্ট করতে বটের Send Messages/Send Media অনুমতি দরকার।
- Telegram-এর নিয়মে যে সদস্য বটকে আগে `/start` দেয়নি তাকে private DM পাঠানো নাও যেতে পারে; সে ক্ষেত্রে গ্রুপে fallback voice/audio যাবে।
- Uploaded audio files `sendAudio` হিসেবে যাবে; Telegram voice notes `sendVoice` হিসেবে যাবে। দুটো ক্ষেত্রেই কোনো warning text পাঠানো হবে না।
