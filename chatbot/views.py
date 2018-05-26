from django.shortcuts import render,redirect
from django.shortcuts import reverse
import random
from django.contrib.auth import authenticate,login,logout
import datetime
from .models import *




def index(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            user = request.user
            context={
                'user_messages':UserMessageHistory.objects.filter(user=user),
                'User':user,
            }
            return render(request,'index.html',context)
        else:
            return redirect('chatbot:login')

    if request.method=="POST":
        user=request.user

        reply=" "
        message=request.POST.get('chat',None)


        if "Hey" in message or "Hi " in message or "Hello" in message or "Yo " in message:
            reply+=helloquery(user)+"<br/>"
        if " wow " in message or "awesome" in message or "love" in message or "wonderful" in message or "thank" in message:
            reply+=thanksquery(user)+"<br/>"
        if "special" in message:
            reply+=special_query(user)+"<br/>"
        if "play" in message or "song" in message:
            reply+=play_song(user)+"<br/>"
        if "color" in message:
            reply+=favcolor_query(user)+"<br/>"
        if "eat" in message or "diet" in message or "food" in message or "recipe" in message:
            reply+= food_query(user)+"<br/>"
        if "route" in message:
            reply+=route_query(user)+"<br/>"
        if "reminder" in message or "note" in message:
            reply+=reminder_query(user)+"<br/>"
        if "horoscope" in message or "fortune" in message:
            reply+=horoscope_query(user)+"<br/>"
        if "friends" in message or "friend" in message:
            reply+=friend_query(user)+"<br/>"
        if reply == " " :
            messageset=["Pardon me!","Didn't getcha!","I didn't understand that!","Nothing syncing!"]
            reply=random.choice(messageset)+"<br/>"



        messagehist_instance = UserMessageHistory.objects.create(user=user, usermessage=message,computermessage=reply)

        context={
            'user_messages': UserMessageHistory.objects.filter(user=user),

        }
        return redirect('{}#msginp'.format(reverse('chatbot:index')))





#prototyping functions:
def helloquery(user):
    greetset= ["Hey","Hello","Hi","Yo"]
    reply=" "+str(random.choice(greetset))+" "
    curr_mem=Member.objects.get(user=user)
    reply+= " " +str(curr_mem.user.username)
    return reply

def thanksquery(user):
    thankset=["Thank you so much! :)","Dont make me blush!","Happy to be at your service!","Thanks!"]
    reply=" "+str(random.choice(thankset))+" "
    curr_mem=Member.objects.get(user=user)
    reply+=" "+str(curr_mem.user.username)
    return reply

def special_query(user):

    mems_with_bday=Member.objects.filter(date_of_birth=datetime.date.today())
    no_of_mems= len(mems_with_bday)
    if no_of_mems == 0:
        reply="No one has their birthday today. Enjoy your day!"
    else:
        reply= " It's "
        for member in mems_with_bday:
            reply+= str(member.user)
            reply += " 's birthday.  <br/>"


        if no_of_mems > 1:
            reply+=". Wish them a happy birthday."
        else:
            reply+=" . Convey your wishes. "

        for member in mems_with_bday:
            reply+=str(member.user)

            wishes=Wish.objects.filter(member=member)
            if len(wishes)==0:
                reply += " hasn't wished for anything ," \
                                          " make sure to get a good gift."
            else:
                reply+=" has wished for "
                for wish in wishes:

                    reply+=str(wish.wish)
                    reply+=" , "

        reply+=". That's for gifting ideas. <br/>"
        reply += " If you are planning on dining out, "
        for member in mems_with_bday:

            reply+=str(member.user)
            reply+=" likes "
            for item in Eat.objects.filter(member=member):
                reply+=str(item.food.food)
                reply += " ,"

            reply+= "  so , choose a suitable restraunt. " \
                    "Else, if you plan to cook at home, you'll need: <ul>" \
                    ""
            for item in Eat.objects.filter(member=member):
                reply+="<li> "+str(item.food.items)
                reply+=" for cooking "
                reply+=" "+str(item.food.food) +". "+"</li>"

            reply+= "</ul> . Make sure to get these items. "

        reply+= "<br/>. Hope you have a good day! . "


    return reply


def food_query(user):
    if user.is_authenticated:
        reply=" "
        fav_foods=Eat.objects.filter(member__user=user)
        if len(fav_foods)==0:
            reply+=" You haven't told me your eating prefernces yet!"

        else:
            reply+=" Wow , your favourite foods are "
            for food in fav_foods:
                reply+=str(food.food.food)+" , "

            reply+=" . You have a good taste." \
                   "You should someday take me out for a dinner" \
                   ",probably."
        return reply
    else:
        reply="I couldn't remember your eating preferences." \
              "You should try logging in first."
        return reply


def favcolor_query(user):
    reply="Your favorite "

    colors=FavColor.objects.filter(member__user=user)

    if len(colors)==0:
        reply="You have not told me about your favourite color . "
    elif len(colors)==1:
        reply+=" color is"
    else :
        reply+=" colors are "

    for c in colors:
        reply += str(c.color.color)

    return reply


def route_query(user):
    reply = " "
    if user.is_authenticated:
        routes=Route.objects.filter(member__user=user).order_by('avg_time')
        for route in routes:
            route.avg_time=(route.avg_time+route.time_today)/2

        if len(routes)==0:
            reply+=" You haven't told me about how you travel to your workplace yet!"
        else:
            reply += " You can travel by " + str(len(routes))
            reply+= " routes which are : "
            for road in routes:
                reply+=" Route < via "
                for stop in road:
                    reply+=str(road.stop1)+" , "
                    reply+=str(road.stop2)
                    reply+=" to "
                    reply+=str(road.dest)

    else:
        reply+=" I've got no idea about your travel pattern. I urge you to " \
              "login and try again."

    return reply

def reminder_query(user):
    if user.is_authenticated:
        reply=" "
        reminders=Reminder.objects.filter(member__user=user)
        if len(reminders)==0:
            reply+=" You have no reminders"

        else :
            reply+=" You have " + str(len(reminders))+" reminders"
            reply+=" and they read out to be as follows:"

            for r in reminders:
                reply+="<hr/>"+str(r.reminder)+"<hr/>"

    else:
        reply="You should try logging in to see your reminders"
    return reply

def horoscope_query(user):
    if user.is_authenticated:
        mem=Member.objects.get(user=user)
        if mem.zodiac is not None:
            reply = " Your horscope reads like this: <br/>"+str(mem.zodiac.desc)

        else:
            reply = "Please update your zodiac sign in the update " \
                    "section and try agian!"

    else:
        reply="You should try logging in to view your fortune.!"
    return reply

def friend_query(user):
    if user.is_authenticated:
        reply=" "
        friends = Friend.objects.filter(member__user=user)
        if len(friends)==0:
            reply+=" None of your friends have their birthdays today"
        else:
            reply+="Today is "
            for fr in friends:
                reply+=str(fr.friend_name)+" ,"
            reply+=" 's birthday. Wish them a happy birthday."
    else:
        reply="You should login to see if its your friends' birthdays"
    return reply

def play_song(user):
    if user.is_authenticated:
        reply=" "
        songs=FavSong.objects.filter(member__user=user)
        if len(songs)==0:
            reply+=" Do you not like any song? Seriously? You " \
                   "should be more honest with me!"
        else:
            reply+=" Here's a list of songs you like:<ul>"
            for song in songs:

                reply+="<li>"+str(song.song.name) +" by " +str(song.song.artist)+"</li>"
            reply+="</ul>"
    else:
        reply="You should login and then try to access your song preference list"
    return reply



def userlogin(request):
    if request.method=="POST":
        username=request.POST.get('uname',None)
        password=request.POST.get('pword',None)
        guest=authenticate(username=username,password=password)

        if guest is not None:
            if guest.is_active:
                login(request,guest)
                return redirect('chatbot:index')

    return render(request,'login.html',context={'error':"Invalid Credentials"})




#User REG View

def userreg(request):
    if request.method=="GET":
        context={
            'zodiac_choices':m_zodiac.objects.all(),
        }
        return render(request,'userreg.html',context)

    if request.method=="POST":
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        user_instance=User.objects.create(username=username,password=password,is_active=True)
        user_instance.set_password(password)
        user_instance.save()
        member_instance=Member.objects.get(user=user_instance)
        dob=request.POST.get('dob',None)
        zodiac=request.POST.get('zod',None)
        zodiac_instance=m_zodiac.objects.get(sl_no=zodiac)
        member_instance.zodiac=zodiac_instance
        member_instance.date_of_birth=dob
        member_instance.save()
        return redirect('{}#loggin'.format(reverse('chatbot:login')))


def ulogout(request):
    logout(request)
    return redirect('{}#loggin'.format(reverse('chatbot:login')))