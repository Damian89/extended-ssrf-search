# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Damian Schwyrz

import sys

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x\n")
    sys.exit(1)

import ssl
import queue
import time

from inc.Config import *
from inc.Tests import *
from inc.Worker import *

ssl._create_default_https_context = ssl._create_unverified_context


def main():
    config = Config()
    tests = Tests(config).tests

    print("Requests to be made: {}".format(len(tests)))
    print(
        "Waiting {} seconds... enough time to kill it, if thats too many requests ;)".format(
            config.sleep_before_testing
        )
    )

    time.sleep(config.sleep_before_testing)

    queue_all = queue.Queue()

    threads = []

    for i in range(0, config.max_threads):
        print("\033[32m[ i ]\033[0m Worker {} started...".format(i))
        worker = Worker(config, queue_all, i)
        worker.setDaemon(True)
        worker.start()
        threads.append(worker)

    for data in tests:
        queue_all.put(data)

    for item in threads:
        item.join()


if __name__ == "__main__":
    main()
