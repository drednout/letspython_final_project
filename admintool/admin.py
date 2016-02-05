from django.contrib import admin
import redis
from models import Players, PlayerSessions, LogGameEvents, PlayerAchievements, PlayerStats


class PlayerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
        redis_con.zadd('scores', obj.xp, obj.id)

admin.site.register([PlayerAchievements, PlayerStats, PlayerSessions, LogGameEvents])
admin.site.register(Players, admin_class=PlayerAdmin)
