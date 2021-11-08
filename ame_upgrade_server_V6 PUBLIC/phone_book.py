from twilio.rest import Client

# for contacts (name and number)
class contacts:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.number


# getting all the information needed to start the bot (tech num comp nums and what he can do
class tw_numbers(contacts):
    def __init__(self, tech, ame1, ame2, car_keys, name, number):
        super().__init__(name, number)
        self.number = number
        self.tech = tech.number
        self.ame1 = ame1.number
        self.ame2 = ame2.number
        self.car_keys = car_keys
        self.chat = True
        self.list_tech = []
        self.techs_answers_for_job = []
        self.pending_jobs = []
        self.tmp_comp_num = ame1.number


# TWILLIO
account_sid = '**************'
auth_token = '**************'
client = Client(account_sid, auth_token)

# bar and google
google_num = contacts('google_num', '+18883334441')
bar_num = contacts('bar_num', '+18883334441')

# TW #
PALM_bot = contacts('PALM_bot', '+18883334441')
georgia_bot = contacts('gerogia_bot', '+18883334441')
detroid_bot = contacts('detoid_bot', '+18883334441')
stockton_bot = contacts('stockton_bot', '+18883334441')
atlanta_bot = contacts('atlanta_bot', '+18883334441')

tw = [PALM_bot, georgia_bot, detroid_bot, stockton_bot, atlanta_bot]

# Techs numbers
israel_palm = contacts('israel_palm', '+18883334441')
tech_gerogia = contacts('tech_gerogia', '+18883334441')
detroid_tech = contacts('detroid_tech', '+18883334441')
or_stockton = contacts('or_stockton', '+18883334441')
tech_atalanta_thomas = contacts('tech_atalanta_thomas', '+18883334441')

techs = [israel_palm, detroid_tech, tech_gerogia, bar_num, tech_atalanta_thomas, or_stockton]

# AME_COMPS
ame_close_in = contacts('ame_close_in', '+18883334441')
ane_job_geo = contacts('ame_job_geo', '+18883334441')
ane_update_geo = contacts('ame_job_geo', '+18883334441')
closing_line_detroid = contacts('closing_line_detroid', '+18883334441')
palm_ame_num = contacts('pam_jobs', '+18883334441')
palm_ame_2 = contacts('palm_updates', '+18883334441')
detroid_jobs = contacts('detroid_jobs', '+18883334441')
detroid_updates = contacts('detroid_updates', '+18883334441')
stockton_jobs = contacts('stockton_jobs', '+18883334441')
stockton_updates = contacts('stockton_updates', '+18883334441')
atlanta_jobs = contacts('atlanta_jobs', '+18883334441')
atlanta_updates = contacts('atlanta_updates', '+18883334441')

ame = [ane_job_geo, ane_update_geo, palm_ame_2, palm_ame_num, detroid_updates,
       detroid_jobs, stockton_jobs, stockton_updates, atlanta_jobs, atlanta_updates]

all_contacts = [techs, ame, tw]

not_getting_calls = [tech_gerogia.number, detroid_tech.number, google_num.number, israel_palm.number,
                     or_stockton.number, tech_atalanta_thomas.number]
# BOTS!
detroid = tw_numbers(detroid_tech, detroid_jobs,
                     detroid_updates, "no", detroid_bot.name, detroid_bot.number)
georgia = tw_numbers(tech_gerogia, ane_job_geo,
                     ane_update_geo, "yes", georgia_bot.name, georgia_bot.number)
palm = tw_numbers(israel_palm, palm_ame_num,
                  palm_ame_2, "yes", PALM_bot.name, PALM_bot.number)
stockton = tw_numbers(or_stockton, stockton_jobs, stockton_updates, "yes", stockton_bot.name, stockton_bot.number)
atlanta = tw_numbers(tech_atalanta_thomas, atlanta_jobs, atlanta_updates, "no", atlanta_bot.name,
                     atlanta_bot.number)


BOTS = [detroid, georgia, palm, stockton, atlanta]
