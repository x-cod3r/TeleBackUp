import os
import time
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterVideo, InputMessagesFilterAudio

API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE_NUMBER = 'YOUR_PHONE_NUMBER'  # with country code
SOURCE_CHANNEL = '@YourSourceChannelOrGroup'
DESTINATION_CHANNEL = '@YourDestinationChannelOrGroup'

# Filters for different types of content
FILTERS = [InputMessagesFilterDocument, InputMessagesFilterVideo, InputMessagesFilterAudio]

SLEEP_INTERVAL = 10  # sleep for 10 seconds between requests, adjust as needed

async def backup_channel(client):
    async for msg_filter in FILTERS:
        async for message in client.iter_messages(SOURCE_CHANNEL, filter=msg_filter):
            # Download the media
            file_path = await message.download_media()
            
            # Sleep to ensure we don't hit rate limits
            time.sleep(SLEEP_INTERVAL)
            
            # Upload it to the destination channel
            await client.send_file(DESTINATION_CHANNEL, file_path)
            
            # Sleep again
            time.sleep(SLEEP_INTERVAL)
            
            # Remove the file from the local system
            os.remove(file_path)

with TelegramClient('anon', API_ID, API_HASH) as client:
    client.start(phone=PHONE_NUMBER)
    client.loop.run_until_complete(backup_channel(client))
