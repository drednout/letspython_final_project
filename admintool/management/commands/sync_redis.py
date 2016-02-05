from django.core.management.base import BaseCommand
from admintool.models import Players
import redis

from final.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class Command(BaseCommand):

    def handle(self, *args, **options):
        for player in Players.objects.all():
            redis_con = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
            redis_con.zadd('scores', player.xp, player.id)
