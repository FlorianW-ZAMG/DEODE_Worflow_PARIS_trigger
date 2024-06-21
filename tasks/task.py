"""SimplePluginExample."""

import datetime as dt
import os

from deode.logs import logger
from deode.tasks.base import Task
from deode.datetime_utils import as_datetime
from deode.tasks.batch import BatchJob
#from ..methods import ExampleMethod

class init_run(Task):
    """Example task 1."""

    def __init__(self, config):
        """Construct object.

        Args:
            config (deode.ParsedConfig): Configuration
        """
        Task.__init__(self, config, __name__)

        #self.basetime = self.config["general.times.basetime"]
        self.basetime = dt.datetime.today().date() 
        self.delay = self.config["paris_delay"]
        self.setup = self.config["task.args.setup"]

    def execute(self):
        """Execute the example."""
        logger.info("config: {}", self.delay)
        logger.info("setup: {}", self.setup)
        logger.info("delay: {}", self.delay[self.setup])
        rundate = as_datetime(self.basetime) - dt.timedelta(days=self.delay[self.setup])
        logger.info("rundate: {}", rundate.date())
        batch = BatchJob(os.environ)
        batch.run("which ls")
        logger.info("DONE")
