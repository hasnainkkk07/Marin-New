import html
import json
import os
from typing import List, Optional

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update, TelegramError)
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from Nobara import (
    DEV_USERS,
    OWNER_ID,
    KAZUHA_ID,
    DRAGONS,
    SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from Nobara.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    wolve_plus,
)
from Nobara.modules.helper_funcs.extraction import extract_user
from Nobara.modules.log_channel import gloggable
import Nobara.modules.sql.nation_sql as sql
from telegram.ext.dispatcher import run_async
from Nobara.modules.helper_funcs.decorators import nobaracmd

def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        return "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        return "This does not work that way."

    else:
        return None

@nobaracmd(command='addsudo')
@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in DRAGONS:
        message.reply_text("This member is already a Sudo user")
        return ""

    if user_id in DEMONS:
        rt += "Requested to promote a Demon user to Sudo."
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Requested to promote a Wolf user to Sudo."
        WOLVES.remove(user_id)

    # will add or update their role
    sql.set_royal_role(user_id, "sudos")
    DRAGONS.append(user_id)

    update.effective_message.reply_text(
        rt
        + "\nSuccessfully promoted {} to Sudo!".format(
            user_member.first_name
        )
    )

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@nobaracmd(command='adddemon')
@sudo_plus
@gloggable
def adddemon(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in DRAGONS:
        rt += "Requested to demote this Sudo to Demon"
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("This user is already a Demon user.")
        return ""

    if user_id in WOLVES:
        rt += "Requested to promote this Wolf user to Demon"
        WOLVES.remove(user_id)

    sql.set_royal_role(user_id, "demons")
    DEMONS.append(user_id)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a Demon user!"
    )

    log_message = (
        f"#DEMON\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@nobaracmd(command='addwolf')
@sudo_plus
@gloggable
def addwolf(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in DRAGONS:
        rt += "This member is a Sudo user, Demoting to wolves user."
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a Demon user, Demoting to wolves user."
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("This user is already a wolves user.")
        return ""

    sql.set_royal_role(user_id, "wolves")
    WOLVES.append(user_id)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a wolves user!"
    )

    log_message = (
        f"#WOLVELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@nobaracmd(command='addtiger')
@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in DRAGONS:
        rt += "This member is a Sudo user, Demoting to Tiger."
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a Demon user, Demoting to Tiger."
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "This user is already a wolves user, Demoting to tiger."
        WOLVES.remove(user_id)

    if user_id in TIGERS:
        message.reply_text("This user is already a tiger.")
        return ""

    sql.set_royal_role(user_id, "tigers")
    TIGERS.append(user_id)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a Tiger Nation!"
    )

    log_message = (
        f"#TIGER\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@nobaracmd(command='removesudo')
@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in DRAGONS:
        message.reply_text("Requested to demote this user to Civilian")
        DRAGONS.remove(user_id)
        sql.remove_royal(user_id)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a Sudo user!")
        return ""


@nobaracmd(command='rmdemon')
@sudo_plus
@gloggable
def rmdemon(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in DEMONS:
        message.reply_text("Requested to demote this user to Civilian")
        DEMONS.remove(user_id)
        sql.remove_royal(user_id)

        log_message = (
            f"#UNDEMON\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a Demon user!")
        return ""


@nobaracmd(command='rmwolf')
@sudo_plus
@gloggable
def rmwolf(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in WOLVES:
        message.reply_text("Demoting to normal user")
        WOLVES.remove(user_id)
        sql.remove_royal(user_id)

        log_message = (
            f"#UNWOLF\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a wolves user!")
        return ""


@nobaracmd(command='rmtiger')
@sudo_plus
@gloggable
def rmtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id in TIGERS:
        message.reply_text("Demoting to normal user")
        TIGERS.remove(user_id)
        sql.remove_royal(user_id)

        log_message = (
            f"#UNTIGER\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Tiger Nation!")
        return ""



@nobaracmd(command='wolflists')
@wolve_plus
def wolflists(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Neptunia Nations :</b>\n"
    for each_user in WOLVES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

@nobaracmd(command='tigers')
@wolve_plus
def Tigers(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Tigers :</b>\n"
    for each_user in TIGERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

@nobaracmd(command=["demonlist", "demons"])
@wolve_plus
def demonlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Sakura Nations :</b>\n"
    for each_user in DEMONS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

@nobaracmd(command=["sudolist", "royals"])
@wolve_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(DRAGONS) - set(DEV_USERS))
    reply = "<b>Known Royals :</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

@nobaracmd(command=["devlist", "Rulers"])
@wolve_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(DEV_USERS) - {OWNER_ID} - {KAZUHA_ID})
    reply = "<b>Rulers :</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


from Nobara.modules.language import gs

def get_help(chat):
    return gs(chat, "nation_help")


__mod_name__ = "Nations"
