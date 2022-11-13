from django.shortcuts import render, HttpResponse, redirect
from SiseWeb.utils.MyService import MyService
from SiseWeb.utils.MyService import LoginService
from django.utils.safestring import mark_safe


# Create your views here.


def Login(request):
    request.session.clear()
    if request.method == "GET":
        return render(request, "Login.html")
    username = request.POST.get('username')
    password = request.POST.get('password')
    myService = LoginService(username, password)
    status = myService.checkStatus()
    if status:
        request.session['info'] = {'id': username, 'password': password}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/")
    else:
        error = "用户名或密码错误"
    return render(request, 'Login.html', {"error": error})


def Logout(request):
    request.session.clear()
    return redirect("Login.html")


def index(request):
    if request.method == "GET":
        username = request.session.get("info")["id"]
        password = request.session.get("info")["password"]
        myService = MyService(username, password)
        stu_info = myService.getStudentInfo()
        credit_info = myService.getCreditInfo()
        context = {
            "stu_info": stu_info,
            "credit_info": credit_info
        }
    return render(request, "index.html", context)


def CurrentClass(request):
    if request.method == "GET":
        username = request.session.get("info")["id"]
        password = request.session.get("info")["password"]
        myService = MyService(username, password)
        current_class = myService.getCurrentClass()
        context = {
            "current_class": current_class
        }
    return render(request, "CurrentClass.html", context)


def ElectiveCourses(request):
    if request.method == "GET":
        username = request.session.get("info")["id"]
        password = request.session.get("info")["password"]
        myService = MyService(username, password)
        elective_class = myService.getElectiveClass()
        context = {
            "elective_class": elective_class
        }
    return render(request, "ElectiveClass.html", context)


def Attendance(request):
    username = request.session.get("info")["id"]
    password = request.session.get("info")["password"]
    myService = MyService(username, password)
    select = mark_safe("".join(myService.getAllSelect()))
    if request.method == "GET":
        year, TruancyTime, truancy_list = myService.getNowAttendance()
        context = {
            "year": year,
            "TruancyTime": TruancyTime,
            "truancy_list": truancy_list,
            "select": select,
        }

        return render(request, "Attendance.html", context)
    value = request.POST.get("yearSemester")
    year, TruancyTime, truancy_list = myService.getYearAttendance(value)
    context = {
        "year": year,
        "TruancyTime": TruancyTime,
        "truancy_list": truancy_list,
        "select": select,
    }
    return render(request, "Attendance.html", context)


def AllClass(request):
    username = request.session.get("info")["id"]
    password = request.session.get("info")["password"]
    myService = MyService(username, password)
    cls_list = myService.GetAllClass()
    context = {
        "cls_list": cls_list,
    }
    return render(request, "Class.html", context)


def ClassSchedule(request):
    username = request.session.get("info")["id"]
    password = request.session.get("info")["password"]
    myService = MyService(username, password)
    schoolyear_str, semester_str = myService.getScheduleSelect()
    schoolyear_str = mark_safe(schoolyear_str)
    semester_str = mark_safe(semester_str)
    if request.method == "GET":
        title, week, schedule_time, cls_list = myService.getCurrentClassSchedule()
        context = {
            "title": title,
            "week": week,
            "schedule_time": schedule_time,
            "cls_list": cls_list,
            "schoolyear_str": schoolyear_str,
            "semester_str": semester_str
        }
        return render(request, "ClassSchedule.html", context)
    schoolyear = request.POST.get("schoolyear")
    semester = request.POST.get("semester")
    title, week, schedule_time, cls_list = myService.getYearSchedule(schoolyear, semester)
    context = {
        "title": title,
        "week": week,
        "schedule_time": schedule_time,
        "cls_list": cls_list,
        "schoolyear_str": schoolyear_str,
        "semester_str": semester_str
    }
    return render(request, "ClassSchedule.html", context)


def ExamSchedule(request):
    username = request.session.get("info")["id"]
    password = request.session.get("info")["password"]
    myService = MyService(username, password)
    cls_list = myService.getExamSchedule()
    context = {
        "cls_list": cls_list
    }
    return render(request, "ExamSchedule.html", context)


def PeacetimePerformance(request):
    username = request.session.get("info")["id"]
    password = request.session.get("info")["password"]
    myService = MyService(username, password)
    cls_info = myService.getPeaceTimeCls()
    if request.method == "GET":
        couse_id = cls_info[0]["courseid"]
        schoolyear = cls_info[0]["schoolyear"]
        semester = cls_info[0]["semester"]
        cls_title, cls_teacher, cls_list = myService.getPeacetimeScore(couse_id, schoolyear, semester)
        context = {
            "cls_title": cls_title,
            "cls_teacher": cls_teacher,
            "cls_info": cls_info,
            "cls_list": cls_list
        }
        return render(request, "PeacetimePerformance.html", context)
    value = str(request.POST.get("course")).split("-")
    couse_id = value[0]
    schoolyear = value[1]
    semester = value[2]
    cls_title, cls_teacher, cls_list = myService.getPeacetimeScore(couse_id, schoolyear, semester)
    context = {
        "cls_title": cls_title,
        "cls_teacher": cls_teacher,
        "cls_info": cls_info,
        "cls_list": cls_list
    }
    return render(request, "PeacetimePerformance.html", context)


def About(request):
    return render(request, "About.html")
