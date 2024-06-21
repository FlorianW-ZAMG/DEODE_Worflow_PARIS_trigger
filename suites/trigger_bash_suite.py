import os
import ecflow as ec

def create_family_experiment(exp):
    return ec.Family(
        exp,
        ec.Task("start_paris", ec.Time("07:00")),
        ec.RepeatDay(1),
    )

print("Creating suite definition")

experiments = ["init_500m", "init_200m"]

home = "/home/kmw/projects/Deode-Prototype/trigger_plugin"

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
        ECF_STATUS_CMD=ecf_status_cmd
    )
)

for exp in experiments:
    fam = defs.trigger_paris.add_family(exp)
    task = fam.add_task("start_paris")
    task.add_cron(ec.Cron("07:00"))

print("Checking job creation: .ecf -> .job0")
print(defs.check_job_creation())

print("Saving definition to file 'trigger_paris.def'")
defs.save_as_defs("trigger_paris.def")

# Start suite
ci = ec.Client()
#ci.load("trigger_paris.def")
ci.replace("/trigger_paris", "trigger_paris.def")

ci.begin_suite("/trigger_paris")