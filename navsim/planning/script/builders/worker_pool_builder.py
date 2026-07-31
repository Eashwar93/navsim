import logging
from typing import Union

from hydra.utils import instantiate
from nuplan.planning.script.builders.utils.utils_type import is_target_type, validate_type
from nuplan.planning.utils.multithreading.worker_parallel import SingleMachineParallelExecutor
from nuplan.planning.utils.multithreading.worker_pool import WorkerPool
from nuplan.planning.utils.multithreading.worker_sequential import Sequential
from omegaconf import DictConfig
from py123d.common.execution.process_pool_executor import ProcessPoolExecutor
from py123d.common.execution import Executor

logger = logging.getLogger(__name__)


def build_worker(cfg: DictConfig) -> Union[WorkerPool, Executor]:
    """
    Builds the worker. It mimics the behavior of the original build_worker function from navsim.planning.script.builders.worker_pool_builder,
    but it is adapted to work with the new Executor class from py123d.common.execution as well.
    
    :param cfg: DictConfig. Configuration that is used to run the experiment.
    :return: Instance of WorkerPool or Executor.
    """
    logger.info("Building WorkerPool...")
    worker: Union[WorkerPool, Executor] = (
        instantiate(cfg.worker)
        if (is_target_type(cfg.worker, SingleMachineParallelExecutor) or is_target_type(cfg.worker, Sequential) or is_target_type(cfg.worker, ProcessPoolExecutor))
        else instantiate(cfg.worker, output_dir=cfg.output_dir)
    )
    validate_type(worker, Union[WorkerPool, Executor])

    logger.info("Building WorkerPool...DONE!")
    return worker
