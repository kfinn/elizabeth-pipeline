from datetime import datetime
import cli.log
import traceback
import logging

from generate_nuclear_masks import generate_nuclear_masks_cli_str

from models.paths import *
from models.swarm_job import SwarmJob

SWARM_SUBJOBS_COUNT = 5

class GenerateAllNuclearMasksJob:
  def __init__(self, source, destination):
    self.source = source
    self.destination = destination
    self.logger = logging.getLogger()

  def run(self):
    SwarmJob(
      self.destination_path,
      self.job_name,
      self.jobs,
      SWARM_SUBJOBS_COUNT
    ).run()

  @property
  def job_name(self):
    if not hasattr(self, "_job_name"):
      self._job_name = "generate_all_nuclear_masks_%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    return self._job_name    

  @property
  def source_path(self):
    if not hasattr(self, "_source_path"):
      self._source_path = source_path(self.source)
      if not self._source_path.is_dir():
        raise Exception("image directory does not exist")
    return self._source_path

  @property
  def destination_path(self):
    if not hasattr(self, "_destination_path"):
      self._destination_path = destination_path(self.destination)
    return self._destination_path
  
  @property
  def jobs(self):
    if not hasattr(self, "_jobs"):
      self._jobs = [
        generate_nuclear_masks_cli_str(source_filename, self.destination) for source_filename in self.source_filenames
      ]
    return self._jobs

  @property
  def source_filenames(self):
    return self.source_path.glob("*_nuclear_segmentation.npy")

@cli.log.LoggingApp
def generate_all_nuclear_masks(app):
  try:
    GenerateAllNuclearMasksJob(
      app.params.source,
      app.params.destination,
    ).run()
  except Exception as exception:
    traceback.print_exc()

generate_all_nuclear_masks.add_param("source")
generate_all_nuclear_masks.add_param("destination")

if __name__ == "__main__":
  generate_all_nuclear_masks.run()
