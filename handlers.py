from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.utils import get_user_stats, order_account
from bot.config import ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Produk", callback_data="produk")],
        [InlineKeyboardButton("📊 Statistik", callback_data="statistik")],
        [InlineKeyboardButton("💰 Saldo & Top-Up", callback_data="saldo")],
        [InlineKeyboardButton("🛒 Beli Akun", callback_data="order")],
        [InlineKeyboardButton("ℹ️ Bantuan", callback_data="bantuan")],
    ]
    await update.message.reply_text("Selamat datang di *Auto Order Bot* 🚀", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "produk":
        await query.edit_message_text("Daftar produk tersedia:\n- SSH/WS\n- VLESS\n- Trojan\n- WireGuard")
    elif query.data == "statistik":
        stats = await get_user_stats(user_id)
        await query.edit_message_text(f"📊 Statistik Anda:\n{stats}")
    elif query.data == "saldo":
        await query.edit_message_text("💰 Menu Saldo & Top-Up:\nSilakan hubungi admin untuk top-up.")
    elif query.data == "order":
        products = ["ssh", "vless", "trojan"]
        keyboard = [[InlineKeyboardButton(p.upper(), callback_data=f"order_{p}")] for p in products]
        await query.edit_message_text("Pilih produk untuk order:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith("order_"):
        product = query.data.replace("order_", "")
        res = await order_account(user_id, product)
        await query.edit_message_text(f"✅ Order berhasil:\n{res}")
    elif query.data == "bantuan":
        await query.edit_message_text("ℹ️ Hubungi admin @username untuk bantuan.")

async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    await update.message.reply_text("👑 Admin Panel:\n- /users\n- /saldo\n- /broadcast")
