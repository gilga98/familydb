from django.contrib import admin
from .models import m_zodiac,m_workpalce,m_color,m_food,m_movie,m_song,Route,Member,Watched_Movie,Wish,Reminder,Eat,FavColor,FavSong,Friend,UserMessageHistory

# Register your models here

admin.site.register(Member)
admin.site.register(Watched_Movie)

admin.site.register(Wish)
admin.site.register(Friend)
admin.site.register(Reminder)
admin.site.register(FavSong)
admin.site.register(FavColor)
admin.site.register(UserMessageHistory)
admin.site.register(Eat)
admin.site.register(Route)
admin.site.register(m_song)
admin.site.register(m_movie)
admin.site.register(m_food)
admin.site.register(m_color)
admin.site.register(m_workpalce)
admin.site.register(m_zodiac)