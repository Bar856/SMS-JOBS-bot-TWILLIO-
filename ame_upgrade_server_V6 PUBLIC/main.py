from flask import Flask, request
from functions import *
from phone_book import *
import threading
import time

app = Flask(__name__)


# MAIN!CODE!

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    number = request.form['From']
    data = request.form['Body']
    to = request.form['To']

    # techs to company הודעה מטכנאי
    def from_tech(data_msg, bot):
        try:
            if bot.chat:
                send_msg2(bot.number, data_msg, bot.tmp_comp_num)
            else:
                if "24/7" in data_msg:
                    send_msg2(bot.number, data_msg, bot.tmp_comp_num)
                else:
                    send_to_goo(bot.number, "{0}: - non chat\n".format(get_name(bot.tech)) + data_msg)
        except Exception as e:
            send_log("error on from_tech() - {0}".format(str(e)), "erors")

    # msgs from me הודעה מגוגל
    def from_google(data_msg, bot):
        try:
            if data_msg == 'sleepnow' or data_msg == "Sleepnow":
                send_to_goo(bot.number, "sleeping for 2 min")
                time.sleep(120)
            elif "totech" in data_msg or "Totech" in data_msg:
                if "totech" in data_msg:
                    new_msg_to2 = cut_works(data_msg.split("totech")[1])
                else:
                    new_msg_to2 = cut_works(data_msg.split("Totech")[1])
                send_msg2(bot.number, new_msg_to2, bot.tech)
            elif data_msg == 'techtocomp t' or data_msg == 'Techtocomp t':
                bot.chat = True
                send_to_goo(bot.number, "changed to chat")
            elif data_msg == 'techtocomp f' or data_msg == 'Techtocomp f':
                bot.chat = False
                send_to_goo(bot.number, "changed to non-chat")
            elif data_msg == 'techtocomp' or data_msg == 'Techtocomp':
                send_to_goo(bot.number, bot.chat)
            elif data_msg == 'sleepnow' or data_msg == "Sleepnow":
                send_to_goo(bot.number, "sleeping for 2 min")
                time.sleep(120)
                # tot2
            elif "tot2" in data_msg:
                new_msg_to2 = cut_works(data_msg.split("tot2")[1])
                send_msg2(bot.number, new_msg_to2, bot.tech)
            elif "Tot2" in data_msg and bot.tech is not None:
                new_msg_to2 = cut_works(data_msg.split("Tot2")[1])
                send_msg2(bot.number, new_msg_to2, bot.tech)
            elif "tocomp" in data_msg or "Tocomp" in data_msg:
                if "tocomp" in data_msg:
                    new_msg_to = data_msg.split("tocomp")[1]
                else:
                    new_msg_to = data_msg.split("Tocomp")[1]
                send_msg2(bot.number, new_msg_to, bot.tmp_comp_num)

        except Exception as e:
            send_log("error on from_google() - {0}" + str(e), "erors")

    # company to techs הודעה מהחברה
    def from_comp(data_msg, from_msg, bot):
        try:
            # chk msg from comp
            chk_msg = chk_msg_from_comp(data_msg)
            job_id = get_job_id(data_msg)
            cut_msg = cut_works(data_msg)
            if chk_msg == "2":
                make_call(bot.number, bar_num)
                send_msg2(bot.number, "HOW MUCH TECH NEED!!!!!", bar_num.number)

            elif chk_msg == "1" or chk_msg == "5":
                send_msg2(bot.number, "Credit card/Unread", bar_num.number)

            elif bot.car_keys == 'no' and chk_msg == "4":
                send_msg2(bot.number, "pass cant do car keys\n{0}".format(data_msg), bot.ame1)
                send_to_goo(bot.number, "cant do sent to comp")

            elif bot.car_keys == 'only' and chk_msg != '4':
                send_msg2(bot.number, "pass only car keys\n{0}".format(data_msg), bot.ame1)
                send_to_goo(bot.number, "pass sent to comp -only car keys")

            elif chk_msg == "3" or chk_msg == '6':
                pass
            elif chk_msg == '7':
                send_msg2(bot.number, cut_msg, bot.tech)

            elif chk_msg == '8':
                send_to_goo(bot.number, "CALLBACK!!!!!!!!!!!!!\n" + cut_msg)
                tech_to_job = get_Tech_from_id(job_id)
                if tech_to_job is not False:
                    send_msg2(bot.number, cut_msg, tech_to_job)
                    send_to_goo(bot.number, "sent to {0}".format(tech_to_job))

            # to tech lead msg
            elif job_id is not False:
                tech_to_job = get_Tech_from_id(job_id)
                if tech_to_job is False and from_msg == bot.ame1:
                    threading.Thread(target=time_comp, args=(bot, data_msg,)).start()
                elif tech_to_job is not False:
                    send_msg2(bot.number, cut_msg, tech_to_job)

                elif tech_to_job is False and from_msg == bot.ame2:
                    send_msg2(bot.number, cut_msg, bot.tech)
            else:
                send_msg2(bot.number, cut_msg, bot.tech)
                send_to_goo(bot.number, "msg without job_id sent to tech1")

        except Exception as e:
            send_log("error on from_comp() - {0}".format(str(e)), "erors")

    # counting time and chk if tech respond to job, if he wont we send k to comp if no we send pass
    def time_comp(bot, data_msg):
        if len(bot.pending_jobs) > 0:
            pass
        else:
            bot.list_tech.clear()
        # csvs
        csv_make(data_msg, get_name(bot.number))
        job_zip = chkzip_comp(data_msg)
        job_id = get_job_id(data_msg)
        bot.pending_jobs.append(job_zip)
        pass_msg = "pass pls dont respond - {0}".format(job_zip)
        tech_k = None
        t = False
        # cut msg
        first_msg = create_1st_msg(data_msg)

        cut_msg = cut_works(data_msg)

        send_msg2(bot.number, first_msg, bot.tech)
        send_to_goo(bot.number, "start countdown - 15 min")
        t_end = time.time() + 60 * 15
        while time.time() < t_end:
            def time_comp_loop():
                if len(bot.list_tech) > 0:
                    for tt in bot.list_tech:
                        # bot.techs_answers_for_job.append(bot.tech)
                        chk_tech = chk_msg_from_tech(tt)
                        zip_tech = chkzip_tech(tt)
                        if zip_tech is not False:
                            if zip_tech == job_zip:
                                if chk_tech == 'chk':
                                    pass
                                elif chk_tech == 'k':
                                    tech_kk = bot.tech
                                    return tech_kk
                                elif chk_tech == "ooa":
                                    pass
                                elif chk_tech is False:
                                    send_msg2(bot.number, 'pls reply with k,pass,ooa + zipcode', bot.tech)
                                    bot.list_tech.remove(tt)
                            elif zip_tech in bot.pending_jobs:
                                pass
                else:
                    pass
                return None

            tech_k = time_comp_loop()
            if tech_k is not None:
                t = True
                break

        if t:
            send_msg2(bot.number, cut_msg, tech_k)
            send_to_goo(bot.number, job_zip + " ASSIGNED " + get_name(tech_k))
            csv_tech_jobs(job_id, tech_k, job_zip)
        else:
            send_to_goo(bot.number, "pass sent - {0}".format(job_zip))
            if len(bot.list_tech) > 0:
                pass
            else:
                send_msg2(bot.number, "PASS\n" + data_msg, bot.ame1)
                send_msg2(bot.number, pass_msg, bot.tech)

        bot.pending_jobs.remove(job_zip)

        # bot.chat = True

    # navigating msgs between all bots numbers and handling them if its comp tech or us
    def what_todo(sender, data_msg, to_msg):
        # todo
        bot = None
        for i in BOTS:
            if to_msg == i.number:
                bot = i
        if bot is None:
            pass
        else:
            if sender == google_num.number:
                from_google(data_msg, bot)
            elif sender == bot.tech:
                bot.list_tech.append(data_msg)
                from_tech(data_msg, bot)
            elif sender == bot.ame1 or sender == bot.ame2:
                bot.tmp_comp_num = sender
                from_comp(data_msg, sender, bot)

    what_todo(number, data, to)
    return number, data


if __name__ == "__main__":
    app.run(debug=True)
