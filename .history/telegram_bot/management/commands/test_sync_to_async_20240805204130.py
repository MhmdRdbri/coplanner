from django.core.management.base import BaseCommand
from channels.db import database_sync_to_async
import asyncio

class Command(BaseCommand):
    help = 'Test database_sync_to_async import'

    async def handle_async(self, *args, **options):
        @database_sync_to_async
        def test_sync():
            return "database_sync_to_async is working!"

        result = await test_sync()
        self.stdout.write(self.style.SUCCESS(result))

    def handle(self, *args, **options):
        asyncio.run(self.handle_async(*args, **options))