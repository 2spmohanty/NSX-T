__author__ = 'smrutim'

"""
Company : VMWare Inc.
                                Apache License
                               Version 2.0, January 2004
                            http://www.apache.org/licenses/
                        Copyright [2019] [Smruti P Mohanty]

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

            http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.



"""

import logging

"""
For Any Code changes.
Please update the READ.md file and here also for quick reference.

"""


def generate_logger(log_file=None):
    log_level = logging.DEBUG
    fh = None
    FORMAT = "%(asctime)s %(levelname)s %(message)s"
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    # Reset the logger.handlers if it already exists.
    if logger.handlers:
        logger.handlers = []
    formatter = logging.Formatter(FORMAT)
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger