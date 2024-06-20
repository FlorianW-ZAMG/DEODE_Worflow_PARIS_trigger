"""Ecflow suites."""

from pathlib import Path

from deode.os_utils import deodemakedirs
from deode.suites.base import (
    EcflowSuiteFamily,
    EcflowSuiteTask,
    EcflowSuiteTrigger,
    EcflowSuiteTriggers,
    SuiteDefinition,
)


class TriggerSuiteDefinition(SuiteDefinition):
    """Definition of suite."""

    def __init__(
        self,
        config,
        dry_run=False,
    ):
        """Construct the definition.

        Args:
            config (deode.ParsedConfig): Configuration file
            dry_run (bool, optional): Dry run not using ecflow. Defaults to False.

        """
        SuiteDefinition.__init__(self, config, dry_run=dry_run)

        self.config = config

        self.suite_name = config["general.case"]

        unix_group = self.platform.get_platform_value("unix_group")
        deodemakedirs(self.joboutdir, unixgroup=unix_group)

        python_template = self.platform.substitute("@DEODE_HOME@/deode/templates/ecflow/default.py")

        exp_list = ["init_500m", "init_250m"]

        for exp in exp_list:
            init_fam = EcflowSuiteFamily(
                        exp,
                        self.suite,
                        self.ecf_files,
                    )
            task1 = EcflowSuiteTask(
                    "init_run",
                    init_fam,
                    config,
                    self.task_settings,
                    self.ecf_files,
#                    trigger=trigger,
                    input_template=python_template,
                )
    
#        trigger=EcflowSuiteTriggers([EcflowSuiteTrigger(task1)])
#
#        task1 = EcflowSuiteTask(
#                "ExampleTask2",
#                self.suite,
#                config,
#                self.task_settings,
#                self.ecf_files,
#                trigger=trigger,
#                input_template=python_template,
#            )
#
#        subtasks = EcflowSuiteFamily(
#                        "Subtasks",
#                        self.suite,
#                        self.ecf_files,
#                        trigger=trigger,
#                    )
#
#        EcflowSuiteTask(
#                "Bashtask",
#                subtasks,
#                config,
#                self.task_settings,
#                self.ecf_files,
#                input_template=bash_job,
#            )