from phone_book import *
import csv
import re
from datetime import datetime

global last_log_error, last_args
last_log_error = ''
last_args = []


# times and calls
def get_time():
    return datetime.today().strftime("%H:%M")


# call tech or no - by time
def to_call():
    if '05:30' < get_time() < '22:30':
        return True
    else:
        return False


# chk msg from comp - credit card, how much tech need, job type(for techs who don't do everything, unread
def chk_msg_from_comp(data):
    if "Credit Card #: " in data or "CVV:" \
            in data or "Exp date:" in data or "Billing zip: " in data or "Card holder:" in data:
        return "1"
    elif "How much does tech need" in data or "HOW MUCH DOES TECH NEED" \
            in data or "HOW MUCH TECH NEED" in data or 'HOW MUCH TECH NEED ' in data or \
            "How much" in data or "how much tech need" in data or "how much" in data or "HOW MUCH" in data:
        return "2"
    elif "Job Type: Car Key Made" in data or "Job Type: Program Car key" in data \
            or "Job Type: Car Ignition Change" in data or "Job Type: Car Key Extraction" in data:
        return "4"
    elif "Giovanni" in data or 'Unread - From' in data:  # jovani!!!!
        return "5"
    elif chkzip_comp(data) is False:
        return '7'
    elif "Please make sure you send the SMS to your assign number for Job Update and Job" in data:
        return "6"
    elif 'This job is a callback' in data:
        return '8'


# Sending msg to google voice number - the monitor of the program
def send_to_goo(tw, data):
    client.messages.create(
        from_=tw,
        body=data,
        to=google_num.number
    )


# Sending msg to number from twillio !!
def send_msg2(tw_num, msg, p_num):
    try:
        client.messages.create(
            from_=tw_num,
            body=msg,
            to=p_num
        )
        send_to_goo(tw_num, "sent to {0}".format(get_name(p_num)))
        send_log("sent to: {0},body:\n {1}".format(get_name(p_num), msg), "msgs")

    except Exception as e:
        send_log("ERROR on send_msg2() error: {0}".format(str(e)), "erors")


# chk k or pass for techs
def chk_msg_from_tech(data):
    # check
    if 'chk' in data or "Chk" in data:
        return 'chk'
    # pass
    elif 'pass' in data or 'Pass' in data or ' pass' in data or ' Pass' in data or 'pass ' in data or 'Pass ' in data \
            or 'pas' in data or 'ooa' in data or 'Ooa' in data or " ooa" in data or "ooa " in data or 'Pas' in data:
        return 'pass'
    # k
    elif 'k' in data or 'K' in data or ' k' in data or ' K' in data or \
            'k ' in data or 'K ' in data:
        return 'k'
    # out of area
    elif 'out of area' in data or "Out of area" in data or "ooa" in data or "Ooa" in data:
        return 'ooa'
    else:
        return False


# clean the msg from company - no id!!!
def cut_work_no_job_id(data):
    deleted_msg = ""
    for line in data.splitlines():
        if "American" in line or "american" in line or "Company:" \
                in line or "company:" in line or "Price:" in line or 'Job: ' in line:
            continue
        elif "Job Type: Car Key Made" in line:
            deleted_msg += "CKM\n"
            continue
        elif "Job Type: Program Car key" in line:
            deleted_msg += "CK Program\n"
            continue
        elif "Job Type: House Lockout" in line:
            deleted_msg += "HLO\n"
            continue
        elif "Job Type: Car Lockout" in line:
            deleted_msg += "CLO\n"
            continue
        elif 'AM' in line or 'PM' in line or 'Suite:' in line or 'Date' in line or 'Time' in line \
                or 'Appointment Info:' in line:
            deleted_msg += line + '\n'
            continue
        elif 'Name: ' in line or 'Phone1: ' in line or 'Phone2: ' in line \
                or 'Job Type: ' in line or 'Address: ' in line or 'Job Notes: ' in line:
            deleted_msg += line.split(': ')[1] + '\n'
        else:
            deleted_msg += line + '\n'

    return deleted_msg


# clean the msg from company - with id!!!
def cut_works(data):
    deleted_msg = "24/7\n"
    for line in data.splitlines():
        if "American" in line or "american" in line or "Company:" \
                in line or "company:" in line or "Price:" in line:
            continue
        elif "Job Type: Car Key Made" in line:
            deleted_msg += "CKM\n"
            continue
        elif "Job Type: Program Car key" in line:
            deleted_msg += "CK Program\n"
            continue
        elif "Job Type: House Lockout" in line:
            deleted_msg += "HLO\n"
            continue
        elif "Job Type: Car Lockout" in line:
            deleted_msg += "CLO\n"
            continue
        elif 'AM' in line or 'PM' in line or 'Suite:' in line or 'Date' in line or 'Time' in line \
                or 'Appointment Info:' in line:
            deleted_msg += line + '\n'
            continue
        elif 'Job: ' in line or 'Name: ' in line or 'Phone1: ' in line or 'Phone2: ' in line \
                or 'Job Type: ' in line or 'Address: ' in line or 'Job Notes: ' in line:
            deleted_msg += line.split(': ')[1] + '\n'
        else:
            deleted_msg += line + '\n'

    return deleted_msg


# send to log file - for ERRORS and msgs log
def send_log(txt, log_name):
    global last_log_error
    if txt != last_log_error:
        with open('./logs/log{0}.txt'.format(log_name), 'a') as fs:
            fs.write(datetime.now().strftime("%d/%m/%Y %H:%M:\n") + txt + "\n")
        print(txt)
        last_log_error = txt
    else:
        pass


# first msg - full address and job type
def create_1st_msg(data):
    deleted_msg = "24/7\n"
    t = False
    s = False
    ad = chk_msg_from_comp(data)
    for line in data.splitlines():
        if 'Job Type: ' in line:
            deleted_msg += line.split(': ')[1] + "\n"
            s = True
            continue
        elif ad == '4' and s:
            s = False
            deleted_msg += line + "\n"
        elif 'Address: ' in line + "\n":
            # deleted_msg += line.split("Address: ")[1] + "\n"
            t = True
        elif t:
            deleted_msg += line + "\n"
        elif "Appointment Info: " in line:
            deleted_msg += line + "\n"
        elif "Job Notes: " in line:
            deleted_msg += line.split(': ')[1] + "\n"
        elif "Please send K" in line:
            pass
    return deleted_msg + "\n\n***Pls reply with 'K' or 'Pass' + ZIPCODE before you update another " \
                         "jobs!***\n"


# search for contact name and return it
def get_name(number):
    for i in all_contacts:
        for i2 in i:
            if number == i2.number:
                return i2.name


# returning the job id of the job
def get_job_id(data):
    job_id = False
    try:
        for line in data.splitlines():
            if 'Job: ' in line:
                job_id = line.split('Job: ')[1]
                break
        return job_id
    except Exception as e:
        send_log("error on get_job_id():{0}" + str(e), "erors")


# csv
def csv_make(data, tw_num):
    job_type = ""
    job_id = ""
    address = ""
    t = False
    for line in data.splitlines():
        if 'Job Type:' in line:
            job_type = line.split('Job Type: ')[1]
        if 'Job:' in line:
            job_id = line.split('Job:')[1]
        if 'Address:' in line:
            address = line.split("Address:")[1]
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        with open('./csvs/jobs_in/' + str(tw_num) + ".csv", 'r') as inp1:
            for row in csv.reader(inp1):
                if row[0] == job_id:
                    t = True
                else:
                    continue
    except:
        pass
    if t is not True and len(job_id) > 1 and len(address) > 1 and len(job_type) > 1:
        open_csv("jobs_in/" + str(tw_num), job_id, job_type, address, time_now)


# appending to existing csv / creating new with our values
def open_csv(name, *args):
    global last_args
    try:
        if args != last_args:
            last_args = args
            with open('./csvs/' + name + ".csv", 'a', newline='') as out:
                writer = csv.writer(out)
                writer.writerow(args)
    except Exception as e:
        send_log("error - open_csv() - {0}" + str(e), "erors")


# 2 techs
def csv_tech_jobs(job_id, tech, job_zip):
    try:
        open_csv("techs_and_jobs", job_id, tech, job_zip, get_name(tech), datetime.now())
    except Exception as e:
        send_log("error on csv_tech_jobs() :{0}" + str(e), "erors")


# chk tech sending the right msg for his job - for k and pass and ooa's
def msg_by_zip_from_tech(zip1, tech):
    try:
        with open('./csvs/' + "techs_and_jobs" + ".csv", 'r') as inp1:
            for row in csv.reader(inp1):
                if row[2] == zip1:
                    if row[1] == tech:
                        return True
        return False
    except Exception as e:
        send_log("error - msg_by_zip_from_tech:{0}" + str(e), "erors")


# make call to tech if he wont respond within 5 min
def make_call(tw_number, tech):
    try:
        if tech not in not_getting_calls:
            client.calls.create(
                twiml='<Response><Say>New New, New Job Available, please reply to message</Say></Response>',
                to=tech.number,
                from_=tw_number
            )
            send_log("call made from:{0} to: {1}".format(tw, get_name(tech)), "msgs_logs")
            send_to_goo(tw_number, "call made to {0}".format(get_name(tech.number)))

    except Exception as e:
        send_log("error on make_call() - {0}".format(str(e)), "erors")


# help to find jobs the techs send k for them
def get_Tech_from_id(job_id):
    try:
        t = False
        with open('./csvs/' + "techs_and_jobs" + ".csv", 'r') as inp1:
            for row in csv.reader(inp1):
                if row[0] == job_id:
                    t = True
                    return row[1]
        if t is False:
            return False
    except Exception as e:
        send_log("error - get_Tech_id_from_id:{0}" + str(e), "erors")


# chk zipcode in msg from comp
def chkzip_comp(data):
    ad = False
    for line in data.splitlines():
        if 'Address: ' in line:
            ad = True
            continue
        elif ad:
            ad = False
            return chkzip_tech(line)
    return ad


# chk zipcode in msg from tech
def chkzip_tech(data):
    for line in data.splitlines():
        postal_code = re.match('^.*(?P<zipcode>\d{5}).*$', line)
        if postal_code is not None:
            return postal_code.groupdict()['zipcode']
    return False
