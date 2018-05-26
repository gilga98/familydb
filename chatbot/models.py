from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class m_zodiac(models.Model):
    sl_no=models.AutoField(primary_key=True)
    sign=models.CharField(max_length=25,null=False,unique=True)
    desc=models.TextField(max_length=1000)

    def __str__(self):
        return str(self.sign)

class m_workpalce(models.Model):
    sl_no = models.AutoField(primary_key=True)
    name= models.CharField(max_length=50)
    ph_num=models.CharField(max_length=12)

    def __str__(self):
        return str(self.name)

class m_song(models.Model):
    sl_no = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    artist=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)

    def __str__(self):
        return str(self.name) + " by " + str(self.artist)


class m_food(models.Model):
    sl_no = models.AutoField(primary_key=True)
    food = models.CharField(max_length=150)
    items = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.food)


class m_movie(models.Model):
    sl_no = models.AutoField(primary_key=True)
    movie_name=models.CharField(max_length=150)

    def __str__(self):
        return str(self.movie_name)

class m_color(models.Model):
    sl_no=models.AutoField(primary_key=True)
    color = models.CharField(max_length=150)


    def __str__(self):
        return str(self.color)



class Member(models.Model):
    sl_no=models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    care_of = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    date_of_birth= models.DateField(null=True)
    zodiac=models.ForeignKey(m_zodiac,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.user.username)

def create_member(sender,**kwargs):
    if kwargs["created"]:
        new_member=Member.objects.create(user=kwargs["instance"])

post_save.connect(create_member,sender=User)



class Friend(models.Model):
    sl_no=models.AutoField(primary_key=True)
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    friend_name= models.CharField(max_length=100)
    friend_dob= models.DateField()

    def __str__(self):
        return str(self.member) + " 's friend " +str(self.friend_name)


class Reminder(models.Model):
    sl_no=models.AutoField(primary_key=True)
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    reminder=models.TextField(max_length=1200)

    def __str__(self):
        return str(self.member) + " 's reminder"

class FavColor(models.Model):
    sl_no=models.AutoField(primary_key=True)
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    color=models.ForeignKey(m_color,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member)+" 's fav color " + str(self.color)

class FavSong(models.Model):
    sl_no=models.AutoField(primary_key=True)
    song=models.ForeignKey(m_song,on_delete=models.CASCADE)
    member=models.ForeignKey(Member,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member) + " 's fav song - " + str(self.song)


class Watched_Movie(models.Model):
    sl_no=models.AutoField(primary_key=True)
    movie = models.ForeignKey(m_movie,on_delete=models.CASCADE)
    member=models.ForeignKey(Member,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie) + " watched by " + str(self.member)


class Eat(models.Model):
    sl_no=models.AutoField(primary_key=True)
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    food=models.ForeignKey(m_food,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.food) +" liked by "+str(self.member)


class Wish(models.Model):
    sl_no=models.AutoField(primary_key=True)
    wish=models.CharField(max_length=150)
    priority=models.PositiveIntegerField()
    member=models.ForeignKey(Member,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member) +" 's wish"



class UserMessageHistory(models.Model):
    usermessage=models.TextField(max_length=10000)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    computermessage=models.TextField(max_length=10000)

    def __str__(self):
        return str(self.user) + " 's message history"


class Route(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    stop1=models.CharField(max_length=20,blank=True)
    stop2=models.CharField(max_length=20,blank=True)
    dest=models.ForeignKey(m_workpalce,on_delete=models.CASCADE)
    avg_time=models.IntegerField()
    time_today=models.IntegerField(blank=True)


    def __str__(self):
        return str(self.member)+" 's route to " +str(self.dest)

