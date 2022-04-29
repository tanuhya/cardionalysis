from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.db.models import Sum

# Create your views here.
def Home(request):
        return render(request, "home.html")

def About(request):
        return render(request, "about.html")

def Contact(request):
    return render(request, "contact.html")

def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    enquiry = Enquiry.objects.all()
    plan = Plan.objects.all()
    equipment = Equipment.objects.all()
    spent=sum(equipment.values_list('price', flat=True))
    member = Member.objects.all()
    amount = sum(member.values_list('initialamount', flat=True))
    e1 = 0
    p1 = 0
    eq1 = 0
    m1 = 0
    
    for i in enquiry:
        e1 += 1
    for i in plan:
        p1 += 1
    for i in equipment:
        eq1 += 1
    for i in member:
        m1 += 1
   
    d = {'e1': e1, 'p1': p1, 'eq1': eq1, 'm1': m1,'amount':amount,'spent':spent}
    return render(request, 'index.html', d)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="registration.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("userhome")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="userlogin.html", context={"login_form":form})

def userhome(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'userhome.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    member=Member.objects.filter(name=request.user.username)
    d={'member':member}
    return render(request,'profile.html',d)

def Login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)

        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, "login.html", d)

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('about')

def logoutuser(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect('about')

def Add_Enquiry(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['emailid']
        a = request.POST['age']
        g = request.POST['gender']
        try:
            Enquiry.objects.create(name=n, contact=c, emailid=e, age=a, gender=g)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_enquiry.html', d)


def View_Enquiry(request):
    if not request.user.is_staff:
        return redirect('login')
    enq = Enquiry.objects.all()
    d = {'enq': enq}
    return render(request, "view_enquiry.html", d)


def Delete_Enquiry(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    enquiry = Enquiry.objects.get(id=pid)
    enquiry.delete()
    return redirect('view_enquiry')


def Add_Equipment(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        n = request.POST['name']
        p = request.POST['price']
        u = request.POST['unit']
        d = request.POST['date']
        de = request.POST['description']

        try:
            Equipment.objects.create(name=n, price=p, unit=u, date=d, description=de)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_equipment.html', d)


def View_Equipment(request):
    if not request.user.is_staff:
        return redirect('login')
    enquipment = Equipment.objects.all()
    d = {'enquipment': enquipment}
    return render(request, "view_equipment.html", d)


def Delete_Equipment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    equipment = Equipment.objects.get(id=pid)
    equipment.delete()
    return redirect('view_equipment')


def Add_Plan(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        n = request.POST['name']
        a = request.POST['amount']
        d = request.POST['duration']

        try:
            Plan.objects.create(name=n, amount=a, duration=d)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_plan.html', d)


def View_Plan(request):
    if not request.user.is_staff:
        return redirect('login')
    plan = Plan.objects.all()
    d = {'plan': plan}
    return render(request, "view_plan.html", d)


def Delete_Plan(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    plan = Plan.objects.get(id=pid)
    plan.delete()
    return redirect('view_plan')

def usermember(request):
    error=""
    if Member.objects.filter(name=request.user.username):
        return redirect('profile')

    if not request.user.is_authenticated:
        return redirect('login')

    else:
        plan1 = Plan.objects.all()
        
        if request.method=="POST":
            n = c = request.POST["name"]
            c = request.POST["contact"]
            e = request.POST["emailid"]
            ag = request.POST["age"]
            g = request.POST["gender"]
            p = request.POST["plan"]
            jd = request.POST["joindate"]
            ed = request.POST["expiredate"]
            I = request.POST["initialamount"]
            plan = Plan.objects.filter(name=p).first()
            try:
                Member.objects.create(name=n,contact=c,emailid=e,age=ag,gender=g,plan=plan,joindate=jd,expiredate=ed,initialamount=I)
                error="no"
            except:
                error="yes"
        d = {'error':error,'plan':plan1}
        return render(request,'usermember.html',d)

def Add_attendance(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method=="POST":
        n = request.user.username
        d = request.POST["date"]
        s = request.POST["status"]
        try:
            Attendance.objects.create(name=n,date=d,status=s)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'add_attendance.html',d)

def View_attendance(request):
    if not request.user.is_authenticated:
        return redirect('login')
    attendance = Attendance.objects.filter(name=request.user.username).order_by("date")
    d = {'attendance':attendance}
    return render(request,'view_attendance.html',d)

def Add_Member(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')

    plan1 = Plan.objects.all()
    if request.method=="POST":
        n = request.POST["name"]
        c = request.POST["contact"]
        e = request.POST["emailid"]
        ag = request.POST["age"]
        g = request.POST["gender"]
        p = request.POST["plan"]
        jd = request.POST["joindate"]
        ed = request.POST["expiredate"]
        I = request.POST["initialamount"]
        plan = Plan.objects.filter(name=p).first()
        try:
            Member.objects.create(name=n,contact=c,emailid=e,age=ag,gender=g,plan=plan,joindate=jd,expiredate=ed,initialamount=I)
            error="no"
        except:
            error="yes"
    d = {'error':error,'plan':plan1}
    return render(request,'add_member.html',d)

def View_Member(request):
    if not request.user.is_staff:
        return redirect('login')
    member = Member.objects.all()
    d = {'member':member}
    return render(request,'view_member.html',d)

def Delete_Member(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    member = Member.objects.get(id=pid)
    member.delete()
    return redirect('view_member')

def attendance(request):
    if not request.user.is_staff:
        return redirect('login')
    attendance = Attendance.objects.all()
    d = {'attendance':attendance}
    return render(request,'attendance.html',d)

def delete_attendance(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    attendance = Attendance.objects.get(id=pid)
    attendance.delete()
    return render('attendance')
