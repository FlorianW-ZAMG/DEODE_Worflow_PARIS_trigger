"""SimplePluginExample."""

import datetime as dt

from deode.logs import logger
from deode.tasks.base import Task
from deode.datetime_utils import as_datetime

#from ..methods import ExampleMethod

class init_run(Task):
    """Example task 1."""

    def __init__(self, config):
        """Construct object.

        Args:
            config (deode.ParsedConfig): Configuration
        """
        Task.__init__(self, config, __name__)

        self.basetime = self.config["general.times.basetime"]

    def execute(self):
        """Execute the example."""
        logger.info("BASETIME:{}", self.basetime)
        logger.info("type:{}", type(self.basetime))
        logger.info("type:{}", type(as_datetime(self.basetime)))
        logger.info("Today:{}", as_datetime(dt.datetime.now().date()))
        logger.info("Todays day: {}", dt.datetime.today().date())
        yesterday = as_datetime(self.basetime) - dt.timedelta(days=1)
        logger.info("Yesterdays date: {}", yesterday)

#class ExampleTask2(Task):
#    """Example task 1."""
#
#    def __init__(self, config):
#        """Construct the task object.
#
#        Args:
#            config (deode.ParsedConfig): Configuration
#        """
#        Task.__init__(self, config, __name__)
#        self.case = self.config.get("general.case")
#
#    def execute(self):
#        """Execute the example."""
#        ExampleMethod().say_hello(self.case)
