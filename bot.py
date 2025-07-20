import os
import subprocess
from pyrogram import Client, filters

API_ID = 15647296  # Replace with your API ID
API_HASH = "0cb3f4a573026b56ea80e1c8f039ad6a"  # Replace with your API HASH
BOT_TOKEN = "7695562666:AAEo8E_GUw30Nki3wTveRjx7wsIEvkdRMAY"

app = Client("gdrive_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_FOLDER = "DownloadedVideos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_from_gdrive(url):
    cmd = f"yt-dlp -f best '{url}' -o '{DOWNLOAD_FOLDER}/%(title)s.%(ext)s'"
    subprocess.run(cmd, shell=True)

@app.on_message(filters.private & filters.text & filters.regex(r'https://drive\.google\.com/'))
async def handle_gdrive(client, message):
    url = message.text.strip()
    await message.reply_text("📥 Downloading from Google Drive...")
    before_files = set(os.listdir(DOWNLOAD_FOLDER))
    download_from_gdrive(url)
    after_files = set(os.listdir(DOWNLOAD_FOLDER))
    new_files = after_files - before_files

    if not new_files:
        await message.reply_text("❌ Download failed.")
        return

    for filename in new_files:
        path = os.path.join(DOWNLOAD_FOLDER, filename)
        size = os.path.getsize(path) / (1024 * 1024)
        await message.reply_text(f"✅ Downloaded: {filename} ({size:.2f} MB)\n📤 Sending the file...")
        try:
            await client.send_document(message.chat.id, document=path, caption=f"🎬 {filename}")
            await message.reply_text("✅ File sent successfully!")
        except Exception as e:
            await message.reply_text(f"❌ Sending file failed: {e}")

app.run()
