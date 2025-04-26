from decouple import config
from telethon import TelegramClient, events
from telethon.errors import UsernameNotOccupiedError, PeerIdInvalidError
from telethon.tl.types import Channel, Chat


API_ID = config("API_ID", cast=int)
API_HASH = config("API_HASH")
BOT_TOKEN = config("BOT_TOKEN")
USERNAME_BOT = config("USERNAME_BOT")

client = TelegramClient("_userinfo", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@client.on(events.NewMessage())
async def message_handler(event: events.NewMessage.Event):
    sender = await event.get_sender()

    if event.message.message.lower() == "/start":
        await event.respond(
            f"Hello {sender.first_name}!\nYour ID: `{sender.id}`\nUsername: @{sender.username if sender.username else 'None'}"
        )

    elif event.message.message == "/help":
        help_text = (
            f"**🔍 Welcome to {USERNAME_BOT}!**\n\n"
            "With this bot, you can easily get the numerical ID of users. Here’s how:\n\n"
            "1. **Forward a message** from the user whose ID you want to retrieve, and send it to this bot.\n"
            "   *Example:* Forward a message and send it here.\n\n"
            "2. **Search by username**: Simply type `@username` and send it to get the user ID.\n"
            "   *Example:* `@username`\n\n"
            f"3. **Use inline search**: Type `{USERNAME_BOT}` in any chat to start an inline search.\n\n"
            "**✉️ Enjoy exploring user IDs with ease!**"
        )
        await event.respond(help_text, parse_mode="markdown")

    elif not event.fwd_from and not event.message.message.startswith("@"):
        sender = await event.get_sender()
        message_info = (
            f"🆔 User ID: `{sender.id}`\n"
            f"👤 Original Sender Name: {sender.first_name or ''} {sender.last_name or ''}\n"
            f"📧 Username: @{sender.username if sender.username else 'None'}\n"
        )
        await event.respond(message_info)

    elif event.message.message.startswith("@"):
        username = event.message.message.split()[0]
        try:
            entity = await client.get_entity(username)

            if isinstance(entity, Channel):
                user_info = (
                    f"📣 Channel Info:\n\n"
                    f"🆔 Channel ID: `-100{entity.id}`\n"
                    f"📢 Title: {entity.title}\n"
                    f"📧 Username: @{entity.username if entity.username else 'None'}\n"
                )
            elif isinstance(entity, Chat):
                user_info = (
                    f"💬 Group Info:\n\n"
                    f"🆔 Group ID: `{entity.id}`\n"
                    f"📢 Title: `{entity.title}`\n"
                    f"📧 Username: @{entity.username if entity.username else 'None'}\n"
                )
            else:
                user_info = (
                    f"👤 User Info:\n\n"
                    f"🆔 User ID: `{entity.id}`\n"
                    f"👥 Name: {entity.first_name or ''} {entity.last_name or ''}\n"
                    f"📧 Username: @{entity.username if entity.username else 'None'}\n"
                )

            await event.respond(user_info)
        except UsernameNotOccupiedError:
            await event.respond("Username not found.")
        except PeerIdInvalidError:
            await event.respond("Invalid entity or username.")
        except Exception:
            pass


@client.on(events.InlineQuery)
async def inline_query_handler(event: events.InlineQuery):
    builder = event.builder
    query = event.text
    if query.startswith("@"):
        username = query[1:]
        try:
            entity = await client.get_entity(username)

            if isinstance(entity, Channel):
                user_info = (
                    f"📣 Channel Info:\n\n"
                    f"🆔 Channel ID: `-100{entity.id}`\n"
                    f"📢 Title: {entity.title}\n"
                    f"📧 Username: @{entity.username if entity.username else 'None'}\n"
                )
                title = "Channel Information"
            elif isinstance(entity, Chat):
                user_info = (
                    f"💬 Group Info:\n\n"
                    f"🆔 Group ID: `{entity.id}`\n"
                    f"📢 Title: {entity.title}\n"
                    f"📧 Username: @{entity.username if entity.username else 'None'}\n"
                )
                title = "Group Information"
            else:
                user_info = (
                    f"👤 User Info:\n\n"
                    f"🆔 User ID: `{entity.id}`\n"
                    f"👥 Name: {entity.first_name or ''} {entity.last_name or ''}\n"
                    f"📧 Username: @{entity.username if entity.username else 'None'}\n"
                )
                title = "User Information"

            result = [builder.article(title=title, text=user_info)]
        except UsernameNotOccupiedError:
            result = [builder.article(title="Error", text="Username not found.")]
        except PeerIdInvalidError:
            result = [builder.article(title="Error", text="Invalid entity or username.")]
        except Exception:
            pass
    else:
        result = [builder.article(title="Error", text='Please enter a valid username starting with "@".')]
    await event.answer(result)

print("✅ Bot is now online and running!")
client.run_until_disconnected()
