import re
import time
import execjs
import requests
from bs4 import BeautifulSoup


class LoginService(object):

    def __init__(self, username, password):

        url = "http://class.seig.edu.cn:7001/sise/login.jsp"

        resp = requests.get(url)

        soup = BeautifulSoup(resp.text, "html.parser")

        rand = soup.find("input", attrs={"id": "random"}).get("value")

        hidden_name = soup.find("input").get("name")

        hidden_value = soup.find("input").get("value")

        cookies = resp.cookies["JSESSIONID"].split("!")[0]

        node = execjs.get()

        ctx = node.compile(open("SiseWeb/utils/sise.js", encoding="utf-8").read())

        funcName = 'getToken("{0}","{1}")'.format(rand, cookies)

        token = ctx.eval(funcName)

        check_url = "http://class.seig.edu.cn:7001/sise/login_check_login.jsp"

        form_data = {
            hidden_name: hidden_value,
            "random": rand,
            "token": token,
            "username": username,
            "password": password
        }
        session = requests.Session()
        resp = session.post(check_url, data=form_data)
        self.resp = resp

    def checkStatus(self):
        obj = re.compile("<script>(?P<message>.*?)</script>")

        if obj.search(self.resp.text.strip()).group("message") == "top.location.href='/sise/index.jsp'":
            return True
        else:
            return False


class MyService(object):

    def __init__(self, username, password):

        self.username = username

        url = "http://class.seig.edu.cn:7001/sise/login.jsp"

        resp = requests.get(url)

        soup = BeautifulSoup(resp.text, "html.parser")

        rand = soup.find("input", attrs={"id": "random"}).get("value")

        hidden_name = soup.find("input").get("name")

        hidden_value = soup.find("input").get("value")

        cookies = resp.cookies["JSESSIONID"].split("!")[0]

        node = execjs.get()

        ctx = node.compile(open("SiseWeb/utils/sise.js", encoding="utf-8").read())

        funcName = 'getToken("{0}","{1}")'.format(rand, cookies)

        token = ctx.eval(funcName)

        check_url = "http://class.seig.edu.cn:7001/sise/login_check_login.jsp"

        form_data = {
            hidden_name: hidden_value,
            "random": rand,
            "token": token,
            "username": username,
            "password": password
        }
        session = requests.Session()
        resp = session.post(check_url, data=form_data)
        self.session = session
        self.resp = resp
        obj = re.compile("studentid=(?P<studentId>.*?)'", re.S)
        obj_stuid = re.compile("studentid=(?P<stuid>.*?)'", re.S)
        url = "http://class.seig.edu.cn:7001/sise/module/student_states/student_select_class/main.jsp"
        resp_main = session.get(url)
        self.resp_main = resp_main
        studentId = obj.search(resp_main.text).group("studentId")
        self.studentId = studentId
        ks = BeautifulSoup(resp_main.text, "html.parser").find("tr", attrs={"title": "考试时间查看"})
        stuid = obj_stuid.search(str(ks)).group("stuid")
        self.stuid = stuid
        info_url = "http://class.seig.edu.cn:7001/SISEWeb/pub/course/courseViewAction.do?method=doMain&studentid=" + studentId
        resp_info = session.get(info_url)
        self.resp_info = resp_info

    def getStudentInfo(self):
        tr_soup = BeautifulSoup(self.resp_info.text, "html.parser").find("table", class_="table1").find("td", class_="tablehead").find("table").find_all("tr")
        td_soup_0 = tr_soup[0].find_all("td", class_="td_left")
        stu_id = td_soup_0[0].text.strip()
        name = td_soup_0[1].text.strip()
        year = td_soup_0[2].text.strip()
        major = td_soup_0[3].text.strip()
        td_soup_1 = tr_soup[1].find_all("td", class_="td_left")
        email = td_soup_1[1].text.strip()
        td_soup_2 = tr_soup[2].find_all("td", class_="td_left")
        xzb = td_soup_2[0].text.strip().split()
        xzb = "".join(xzb)
        headmaster = td_soup_2[1].text.strip()
        instructor = td_soup_2[2].text.strip()
        info = {"stu_id": stu_id, "name": name, "year": year, "major": major, "email": email, "szb": xzb, "headmaster": headmaster, "instructor": instructor}
        return info

    def getCurrentClass(self):
        soup_table = BeautifulSoup(self.resp_info.text, "html.parser").find("table", class_="table").find("tbody").find_all("tr")
        current_list = []
        for tr in soup_table:
            td = tr.find_all("td")
            if td[6].text.strip() == "在读":
                class_id = td[1].text.strip()
                class_name = td[2].text.strip()
                class_credit = td[3].text.strip()
                class_method = td[4].text.strip()
                current_info = {"class_id": class_id, "class_name": class_name, "class_credit": class_credit, "class_method": class_method}
                current_list.append(current_info)
        return current_list

    def getElectiveClass(self):
        soup_table = BeautifulSoup(self.resp_info.text, "html.parser").find_all("table", class_="table")[1].find("tbody").find_all("tr")
        elective_list = []
        for tr in soup_table:
            td = tr.find_all("td")
            class_id = td[0].text.strip()
            class_name = td[1].text.strip()
            class_credit = td[2].text.strip()
            class_method = td[3].text.strip()
            class_year = td[4].text.strip()
            class_score = td[5].text.strip()
            class_getCredit = td[6].text.strip()
            class_prerequisite = td[7].text.strip()
            class_info = {"class_id": class_id, "class_name": class_name, "class_credit": class_credit, "class_method": class_method, "class_year": class_year, "class_score": class_score, "class_getCredit": class_getCredit, "class_prerequisite": class_prerequisite}
            elective_list.append(class_info)
        return elective_list

    def getCreditInfo(self):
        soup_table = BeautifulSoup(self.resp_info.text, "html.parser").find_all("table")[13].find_all("tr")
        a = soup_table[2].find_all("td")[3].text.strip()
        b = soup_table[3].find_all("td")[3].text.strip()
        c = soup_table[4].find_all("td")[3].text.strip()
        d = soup_table[5].find_all("td")[3].text.strip()
        e = soup_table[6].find_all("td")[3].text.strip()
        f = soup_table[7].find_all("td")[1].text.strip()
        CreditInfo = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f}
        return CreditInfo

    def getNowAttendance(self):
        obj = re.compile("gzcode=(?P<code>.*?)'")
        code = obj.search(self.resp_main.text).group("code").replace("%2B", "+")
        params = {
            "method": "doMain",
            "studentID": self.studentId.replace("%2B", "+"),
            "gzcode": code
        }
        resp = self.session.get(f"http://class.seig.edu.cn:7001/SISEWeb/pub/studentstatus/attendance/studentAttendanceViewAction.do", params=params)
        soup = BeautifulSoup(resp.text, "html.parser")
        year = soup.find("select", attrs={"name": "yearSemester"}).find("option", attrs={"selected": "selected"}).text.strip().split(",")
        year = "".join(year)
        TruancyTime = soup.find_all("table")[4].find("td").find_all("td")[1].text.strip()
        table = soup.find("table", class_="table").find_all("tr")[1:]
        truancy_list = []
        for tr in table:
            td = tr.find_all("td")
            class_id = td[0].text
            class_name = td[1].text
            class_detail = td[2].text
            if len(class_detail) != 0:
                class_detail = class_detail.split()
                class_detail = ",".join(class_detail).replace("[", "").replace("]", "")
            truancy_info = {"class_id": class_id, "class_name": class_name, "class_detail": class_detail}
            truancy_list.append(truancy_info)
        return year, TruancyTime, truancy_list

    def getAllSelect(self):
        year = BeautifulSoup(self.resp_info.text, "html.parser").find("table", class_="table1").find("table").find("tr").find_all("td")[5].text.strip() + "1"
        obj = re.compile("gzcode=(?P<code>.*?)'")
        code = obj.search(self.resp_main.text).group("code").replace("%2B", "+")
        params = {
            "method": "doMain",
            "studentID": self.studentId.replace("%2B", "+"),
            "gzcode": code
        }
        resp = self.session.get(f"http://class.seig.edu.cn:7001/SISEWeb/pub/studentstatus/attendance/studentAttendanceViewAction.do", params=params)
        soup = BeautifulSoup(resp.text, "html.parser").find("select", attrs={"name": "yearSemester"}).find_all("option")

        for i in range(len(soup)):
            if soup[i].get("selected") == "selected":
                start_count = i
            if soup[i].get("value") == year:
                end_count = i
        select = soup[start_count:end_count + 1]
        select_str = ""
        for i in select:
            select_str += str(i)
        return select_str

    def getYearAttendance(self, yearsemester):
        params = {
            "method": "doYearTermSelect"
        }
        data = {
            "studentID": self.stuid,
            "studentCode": self.username,
            "yearSemester": yearsemester,
            "doSubmit": "++%B2%E9%BF%B4++"
        }
        truancys_list = []
        resp = self.session.post("http://class.seig.edu.cn:7001/SISEWeb/pub/studentstatus/attendance/studentAttendanceViewAction.do", params=params, data=data)
        soup = BeautifulSoup(resp.text, "html.parser")
        year = soup.find("select", attrs={"name": "yearSemester"}).find("option", attrs={"selected": "selected"}).text.strip().split(",")
        year = "".join(year)
        TruancyTime = soup.find_all("table")[4].find("td").find_all("td")[1].text.strip()
        table = soup.find("table", class_="table").find_all("tr")[1:]
        for tr in table:
            td = tr.find_all("td")
            class_id = td[0].text
            class_name = td[1].text
            class_detail = td[2].text
            if len(class_detail) != 0:
                class_detail = class_detail.split()
                class_detail = ",".join(class_detail).replace("[", "").replace("]", "")
            truancy_info = {"class_id": class_id, "class_name": class_name, "class_detail": class_detail}
            truancys_list.append(truancy_info)
        return year, TruancyTime, truancys_list

    def GetAllClass(self):
        soup = BeautifulSoup(self.resp_info.text, "html.parser")
        class_info = soup.find_all("table")[6].find("tbody").find_all('tr')
        cls_list = []
        for cls in class_info:
            td = cls.find_all('td')
            class_semester = td[0].text
            class_id = td[1].text
            class_name = td[2].text
            class_credit = td[3].text
            class_method = td[4].text
            class_year = td[5].text
            class_score = td[6].text
            class_getCredit = td[7].text
            class_prerequisite = td[8].text
            cls_info = {"class_semester": class_semester, "class_id": class_id, "class_name": class_name, "class_credit": class_credit, "class_method": class_method, "class_year": class_year, "class_score": class_score, "class_getCredit": class_getCredit, "class_prerequisite": class_prerequisite}
            cls_list.append(cls_info)
        return cls_list

    def getCurrentClassSchedule(self):
        resp = self.session.get("http://class.seig.edu.cn:7001/sise/module/student_schedular/student_schedular.jsp")
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.find_all("table")[2].text.strip().split()
        title = " ".join(title)
        week = soup.find_all("table")[4].find_all("td")[2].text.strip()
        schedule_time = soup.find_all("table")[4].find_all("td")[3].text.strip()
        table = soup.find_all("table")[6].find_all("tr")[1:]
        cls_list = []
        for tr in table:
            td = tr.find_all("td")
            td_head = td[0].text.strip()
            td_1 = td[1].text.strip()
            td_2 = td[2].text.strip()
            td_3 = td[3].text.strip()
            td_4 = td[4].text.strip()
            td_5 = td[5].text.strip()
            cls_sch = {"td_head": td_head, "td_1": td_1, "td_2": td_2, "td_3": td_3, "td_4": td_4, "td_5": td_5}
            cls_list.append(cls_sch)
        return title, week, schedule_time, cls_list

    def getScheduleSelect(self):
        resp = self.session.get("http://class.seig.edu.cn:7001/sise/module/student_schedular/student_schedular.jsp")
        soup = BeautifulSoup(resp.text, "html.parser")
        schoolyear = soup.find("select", attrs={"name": "schoolyear"}).find_all("option")
        semester = soup.find("select", attrs={"name": "semester"}).find_all("option")
        schoolyear_str = ""
        semester_str = ""
        for year in schoolyear:
            schoolyear_str += str(year)
        for ter in semester:
            semester_str += str(ter)
        return schoolyear_str, semester_str

    def getYearSchedule(self, schoolyear, semester):
        params = {
            "schoolyear": schoolyear,
            "semester": semester
        }
        resp = self.session.get("http://class.seig.edu.cn:7001/sise/module/student_schedular/student_schedular.jsp", params=params)
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.find_all("table")[2].text.strip().split()
        title = " ".join(title)
        week = soup.find_all("table")[4].find_all("td")[2].text.strip()
        schedule_time = soup.find_all("table")[4].find_all("td")[3].text.strip()
        table = soup.find_all("table")[6].find_all("tr")[1:]
        cls_list = []
        for tr in table:
            td = tr.find_all("td")
            td_head = td[0].text.strip()
            td_1 = td[1].text.strip()
            td_2 = td[2].text.strip()
            td_3 = td[3].text.strip()
            td_4 = td[4].text.strip()
            td_5 = td[5].text.strip()
            cls_sch = {"td_head": td_head, "td_1": td_1, "td_2": td_2, "td_3": td_3, "td_4": td_4, "td_5": td_5}
            cls_list.append(cls_sch)
        return title, week, schedule_time, cls_list

    def getExamSchedule(self):
        params = {
            "method": "doMain",
            "studentid": self.stuid
        }
        resp = self.session.get("http://class.seig.edu.cn:7001/SISEWeb/pub/exam/studentexamAction.do", params=params)
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table", class_="table").find_all("tr")[1:]
        cls_list = []
        for tr in table:
            td = tr.find_all("td")
            cls_id = td[0].text.strip()
            cls_name = td[1].text.strip()
            cls_date = td[2].text.strip()
            cls_time = td[3].text.strip()
            cls_examroom = td[4].text.strip()
            cls_seat = td[6].text.strip()
            cls_info = {"cls_id": cls_id, "cls_name": cls_name, "cls_date": cls_date, "cls_time": cls_time, "cls_examroom": cls_examroom, "cls_seat": cls_seat}
            cls_list.append(cls_info)
        return cls_list

    def getPeaceTimeCls(self):
        obj = re.compile("courseid=(?P<courseid>.*?)&schoolyear=(?P<schoolyear>.*?)&", re.S)
        resp = self.session.get("http://class.seig.edu.cn:7001/sise/module/commonresult/index.jsp")
        soup = BeautifulSoup(resp.text, "html.parser")
        resp.close()
        table = soup.find("table", class_="table1").find_all("tr")[1:]
        cls_list = []
        for tr in table:
            td = tr.find("td")
            cls_name = td.text.strip()
            href = td.find("a").get("href")
            courseid = obj.search(href).group("courseid")
            schoolyear = obj.search(href).group("schoolyear")
            semester = href.split("=")[-1]
            cls_info = {"cls_name": cls_name, "courseid": courseid, "schoolyear": schoolyear, "semester": semester}
            cls_list.append(cls_info)
        return cls_list

    def getPeacetimeScore(self, courseid, schoolyear, senester):
        params = {
            "courseid": courseid,
            "schoolyear": schoolyear,
            "semester": senester
        }
        resp = self.session.get("http://class.seig.edu.cn:7001/sise/module/commonresult/showdetails.jsp", params=params)
        resp.close()
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.find("table").text.strip().split("任课教师与教学班")
        cls_title = title[0].strip()
        cls_teacher = "任课教师与教学班" + title[1].strip()
        table = soup.find_all("table")[1].find_all("tr")[2:]
        cls_list = []
        for tr in table:
            td = tr.find_all("td")
            cls_source = td[0].text.strip()
            cls_percent = td[1].text.strip()
            cls_highest = td[2].text.strip()
            cls_score = td[3].text.strip()
            cls_info = {"cls_source": cls_source, "cls_percent": cls_percent, "cls_highest": cls_highest, "cls_score": cls_score}
            cls_list.append(cls_info)
        table_summary = soup.find_all("table")[3].find_all("tr")[1]
        td_summary = table_summary.find_all("td")
        summary_source = td_summary[0].text.strip()
        summary_percent = td_summary[1].text.strip()
        summary_highest = td_summary[2].text.strip()
        summary_score = td_summary[3].text.strip()
        summary_info = {"cls_source": summary_source, "cls_percent": summary_percent, "cls_highest": summary_highest, "cls_score": summary_score}
        cls_list.append(summary_info)
        return cls_title, cls_teacher, cls_list
