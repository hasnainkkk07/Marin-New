import html
import json
import os
from typing import List, Optional

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update, TelegramError)
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from Raiden import (
    DEV_USERS,
    OWNER_ID,
    KAZUHA_ID,
    WHITELIST_USERS,
    SUPPORT_CHAT,
    DEMONS,
    SUPPORT_USERS,
    dispatcher,
)
from Raiden.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    wolve_plus,
)
from Raiden.modules.helper_funcs.extraction import extract_user
from Raiden.modules.log_channel import gloggable
import Raiden.modules.sql.nation_sql as sql
from telegram.ext.dispatcher import run_async
from Raiden.modules.helper_funcs.decorators import raidencmd

def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        return "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        return "This does not work that way."

    else:
        return None

@raidencmd(command='addsudo')
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

    if user_id in WHITELIST_USERS:
        message.reply_text("This member is already my senpai")
        return ""

    if user_id in DEMONS:
        rt += "Requested to promote a Demon user to Sudo."
        DEMONS.remove(user_id)

    if user_id in SUPPORT_USERS:
        rt += "Requested to promote a Wolf user to Sudo."
        SUPPORT_USERS.remove(user_id)

    # will add or update their role
    sql.set_royal_role(user_id, "sudos")
    WHITELIST_USERS.append(user_id)

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


@raidencmd(command='adddemon')
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

    if user_id in WHITELIST_USERS:
        rt += "Requested to demote this Sudo to Demon"
        WHITELIST_USERS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("This user is already a Demon user.")
        return ""

    if user_id in SUPPORT_USERS:
        rt += "Requested to promote this Wolf user to Demon"
        SUPPORT_USERS.remove(user_id)

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


@raidencmd(command='addwolf')
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

    if user_id in WHITELIST_USERS:
        rt += "This member is a Sudo user, Demoting to wolves user."
        WHITELIST_USERS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a Demon user, Demoting to wolves user."
        DEMONS.remove(user_id)

    if user_id in SUPPORT_USERS:
        message.reply_text("This user is already a wolves user.")
        return ""

    sql.set_royal_role(user_id, "senpais")
    SUPPORT_USERS.append(user_id)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a wolves user!"
    )

    log_message = (
        f"#SENPAILIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@raidencmd(command='removesudo')
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

    if user_id in WHITELIST_USERS:
        message.reply_text("Requested to demote this user to Civilian")
        WHITELIST_USERS.remove(user_id)
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


@raidencmd(command='rmdemon')
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


@raidencmd(command='rmwolf')
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

    if user_id in SUPPORT_USERS:
        message.reply_text("Demoting to normal user")
        SUPPORT_USERS.remove(user_id)
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


@raidencmd(command='wolflists')
@wolve_plus
def wolflists(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Senpais :</b>\n"
    for each_user in SUPPORT_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

@raidencmd(command=["demonlist", "demons"])
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

@raidencmd(command=["sudolist", "royals"])
@wolve_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(WHITELIST_USERS) - set(DEV_USERS))
    reply = "<b>Known Royals :</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

@raidencmd(command=["devlist", "Rulers"])
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


__help__ = f"""
*⚠️ Notice:*
Commands listed here only work for users with special access are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands.

*Ping:*
❍ /ping*:* gets ping time of bot to telegram server
❍ /pingall*:* gets all listed ping times

*Broadcast: (Bot owner only)*
*Note:* This supports basic markdown
❍ /broadcastall*:* Broadcasts everywhere
❍ /broadcastusers*:* Broadcasts too all users
❍ /broadcastgroups*:* Broadcasts too all groups

*Groups Info:*
❍ /groups*:* List the groups with Name, ID, members count as a txt
❍ /leave <ID>*:* Leave the group, ID must have hyphen
❍ /stats*:* Shows overall bot stats
❍ /getchats*:* Gets a list of group names the user has been seen in. Bot owner only
❍ /ginfo username/link/ID*:* Pulls info panel for entire group

`⚠️ Read from top`
Visit @{SUPPORT_CHAT} for more information.
"""


__mod_name__ = "Nations"
