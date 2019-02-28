#!/usr/bin/env python
# coding: utf8

import threading
import http.client
from inc.Color import *
from inc.Connection import Connection as OwnConnection
stopSet = True


class Worker(threading.Thread):
    def __init__(self, config, queue, tid):
        threading.Thread.__init__(self)
        self.queue = queue
        self.tid = tid
        self.config = config

    def run(self):
        global stopSet

        while stopSet:

            try:
                data = self.queue.get(timeout=1)


            except Exception as e:
                stopSet = False
                break

            try:

                conn = OwnConnection(self.config, data)
                conn.connect()
                response = conn.response

                state = self.__make_color_state(response)

                print("{} [Proc: {}] {} [{}] [{}]".format(
                    state,
                    self.tid,
                    data["url"],
                    response.status,
                    data["test_name"]
                ))

            except Exception as e:
                print("{} [Proc: {}] {} [{}] [{}]".format(
                    Color.danger("[ x ]"),
                    self.tid,
                    data["url"],
                    data["test_name"],
                    e
                ))

            self.queue.task_done()

    @staticmethod
    def __make_color_state(response):
        if response.status == 200:
            state = Color.green("[ R ]")
        elif 200 < response.status <= 500:
            state = Color.orange("[ R ]")
        else:
            state = Color.red("[ R ]")
        return state
