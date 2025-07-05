# === Render के लिए बनाया गया अंतिम कोड (Polling) ===

import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
)

# Logging को सेटअप करें
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# टोकन को Secrets से लेना
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# --- बातचीत के स्टेप्स और फोन डेटा (कोई बदलाव नहीं) ---
BRAND, MODEL, RAM = range(3)
phone_models = {
    "Samsung": ["Galaxy S23", "Galaxy A54", "Galaxy M34", "Galaxy F23"],
    "Xiaomi": ["Redmi Note 12 Pro", "Poco F5", "Poco X3 Pro", "Redmi 10"],
    "Realme": ["Realme 11 Pro", "Realme GT Master", "Realme Narzo 50"],
    "Apple": ["iPhone 14 Pro", "iPhone 13", "iPhone 11", "iPhone XR"],
    "Other": ["Low-End Device", "Mid-Range Device", "High-End Device"]
}

# --- बातचीत के फंक्शन्स (कोई बदलाव नहीं) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("नमस्ते! मैं Render पर होस्टेड आपका नया बॉट हूँ।\n\n/sensitivity कमांड का इस्तेमाल करें।")

# ... (बाकी के सारे async फंक्शन्स brand_choice, model_choice, ram_choice, cancel यहाँ आएंगे, उनमें कोई बदलाव नहीं) ...
async def sensitivity_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(brand, callback_data=brand)] for brand in phone_models.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Step 1: अपना मोबाइल ब्रांड चुनें:", reply_markup=reply_markup)
    return BRAND
async def brand_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer(); brand = query.data; context.user_data['brand'] = brand; models = phone_models[brand]; keyboard = [[InlineKeyboardButton(model, callback_data=model)] for model in models]; reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Step 2: अब अपना {brand} मॉडल चुनें:", reply_markup=reply_markup); return MODEL
async def model_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer(); model = query.data; context.user_data['model'] = model; ram_options = ["2-3 GB", "4 GB", "6 GB", "8 GB", "12 GB+"]; keyboard = [[InlineKeyboardButton(ram, callback_data=ram)] for ram in ram_options]; reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Step 3: अपनी रैम (RAM) चुनें:", reply_markup=reply_markup); return RAM
async def ram_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer(); ram = query.data; brand = context.user_data.get('brand', 'N/A'); model = context.user_data.get('model', 'N/A'); general = random.randint(95, 100); red_dot = random.randint(92, 100); scope_2x = random.randint(88, 98)
    if "2-3 GB" in ram: dpi = random.randint(360, 410)
    elif "4 GB" in ram: dpi = random.randint(400, 450)
    else: dpi = random.randint(450, 520)
    result_text = (f"✅ आपके {brand} {model} ({ram}) के लिए सेंसिटिविटी:\n\n🎯 General: {general}\n🎯 Red Dot: {red_dot}\n🎯 2x Scope: {scope_2x}\n🎯 4x Scope: {random.randint(85, 95)}\n🎯 Sniper Scope: {random.randint(75, 88)}\n🎯 Free Look: {random.randint(70, 90)}\n\n✨ (Bonus) DPI: {dpi}\n\nनई सेंसिटिविटी के लिए दोबारा /sensitivity टाइप करें.")
    await query.edit_message_text(text=result_text); return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: await update.message.reply_text("प्रोसेस कैंसिल कर दिया गया है।"); return ConversationHandler.END


# === Render के लिए मुख्य फंक्शन ===
def main() -> None:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set! The bot cannot start.")
        return

    # एप्लीकेशन को बनाएं
    application = Application.builder().token(BOT_TOKEN).build()

    # बातचीत को संभालने वाला Handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("sensitivity", sensitivity_start)],
        states={
            BRAND: [CallbackQueryHandler(brand_choice)],
            MODEL: [CallbackQueryHandler(model_choice)],
            RAM: [CallbackQueryHandler(ram_choice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    # बॉट को चलाना शुरू करें (Polling)
    logger.info("Bot is starting with polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
