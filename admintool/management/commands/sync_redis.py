from django.core.management.base import BaseCommand
from admintool.models import Players
import redis


class Command(BaseCommand):

    def handle(self, *args, **options):
        for player in Players.objects.all():
            redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
            redis_con.zadd('scores', player.xp, player.id)
