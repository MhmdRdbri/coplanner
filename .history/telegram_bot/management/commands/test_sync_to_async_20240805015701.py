from django.core.management.base import BaseCommand
from django.utils.asyncio import sync_to_async
import asyncio

class Command(BaseCommand):
    help = 'Test sync_to_async import'

    def handle(self, *args, **options):
        async def test_async():
            return "sync_to_async is working!"

        result = asyncio.run(sync_to_async(test_async)())
        self.stdout.write(self.style.SUCCESS(result))
