#!/usr/bin/env python
# coding: utf8

import threading
import http.client

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

                if "https" in data["url"]:
                    connection = http.client.HTTPSConnection(data["host"], 443, timeout=self.config.http_timeout)
                else:
                    connection = http.client.HTTPConnection(data["host"], 80, timeout=self.config.http_timeout)

                connection.request(
                    data["method"],
                    data["path"],
                    data["body"],
                    data["headers"]
                )
                response = connection.getresponse()
                connection.close()


                print("\033[32m[ R ]\033[0m [Proc: {}] Request to {} [{}] [{}]".format(
                    self.tid, data["url"], response.status, data["test_name"]
                ))

            except Exception as e:
                print("\033[31m[ x ]\033[0m [Proc: {}] [URL: {}] [{}] Error: {}".format(self.tid, data["url"], data["test_name"], e))

            self.queue.task_done()
