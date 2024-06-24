import os
import datetime as dt
import ecflow as ec

def create_family_experiment(exp):
    return ec.Family(
        exp,
        ec.Task("start_paris", ec.Time("07:00")),
        ec.RepeatDay(1),
    )

print("Creating suite definition")

experiments = {"init_500m": {"delay": 1,
                             "config": "cy46h1_harmonie_arome_paris_500m_cold",
                             "paris_suite": "PARIS_RDP_CY46h1_500M_cold"}, 
               "init_200m": {"delay": 2,
                             "config": "cy46h1_harmonie_arome_paris_200m_warm",
                             "paris_suite": "PARIS_RDP_CY46h1_200M_warm"}}

home = os.getcwd()

ecf_job_cmd = "troika submit -o %ECF_JOBOUT% %SCHOST% %ECF_JOB%"
ecf_kill_cmd = "troika kill %SCHOST% %ECF_JOB%"

ecf_status_cmd = "troika monitor %SCHOST% %ECF_JOB%"

defs = ec.Defs(
    ec.Suite(
        "trigger_paris",
        ECF_INCLUDE=os.path.join(home, "include"),
        ECF_HOME=home,
        ECF_FILES=os.path.join(home, "tasks"),
        QUEUE="nf",
        SCHOST="hpc",
        ECF_JOB_CMD=ecf_job_cmd,
        ECF_KILL_CMD=ecf_kill_cmd,
        ECF_STATUS_CMD=ecf_status_cmd,
        HOME=home
    )
)

basetime = dt.datetime.today().date()
trig_fam = defs.trigger_paris.add_family("initialize")
trig_fam.add_repeat(ec.RepeatDate("YMD", 20240621, 20240622))

for exp in experiments.keys():
  
    fam = trig_fam.add_family(exp)
    fam.add_cron(ec.Cron("08:40"))
    
    # Check whether suite is complete and we can safely run it for current date
    check_suites = fam.add_task("check_suites")
    check_suites.add_event(exp)
    check_suites.add_variable("SETUP", exp)
    check_suites.add_variable("P_SUITE", experiments[exp]["paris_suite"])
    check_suites.add_variable("STATE", "complete")


    task = fam.add_task("start_paris")
    task.add_variable("DELAY", experiments[exp]["delay"])
    task.add_variable("CONFIG", experiments[exp]["config"])
    task.add_label("info", "")
    task.add_trigger("check_suites == complete and check_suites:{0}".format(exp))

"""     check_suites = fam.add_task("safety_check")
    check_suites.add_event(exp)
    check_suites.add_variable("SETUP", exp)
    check_suites.add_variable("P_SUITE", experiments[exp]["paris_suite"])
    check_suites.add_variable("STATE", "running")
    check_suites.add_trigger("start_paris == complete") """


print("Checking job creation: .ecf -> .job0")
print(defs.check_job_creation())

print("Saving definition to file 'trigger_paris.def'")
defs.save_as_defs("trigger_paris.def")

# Start suite
ci = ec.Client()
#ci.load("trigger_paris.def")
ci.replace("/trigger_paris", "trigger_paris.def")

ci.begin_suite("/trigger_paris")
