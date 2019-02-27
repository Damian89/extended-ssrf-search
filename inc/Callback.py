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


class Callback:

    def __init__(self, url, config, case, type):
        self.url = url
        self.config = config
        self.case = case
        self.type = type
        self.hostname = ""
        self.result = ""
        self.name = ""

    def make(self):
        if self.case is "http":
            self.__make_http_callback_url()

        if self.case is "dns":
            self.__make_dns_callback()

    def __make_dns_callback(self):

        if self.type == "default":
            self.result = "{}-{}.{}".format(self.name, self.hostname, self.config.callback)
            return

        if self.type == "exec":
            self.result = "{}.{}-{}.{}".format(self.config.attack_exec_payload, self.name, self.hostname,
                                               self.config.callback)
            return

    def __make_http_callback_url(self):

        if self.type == "default" and self.config.identifier_position == "prepend":
            self.result = "http://{}-{}.{}".format(self.name, self.hostname, self.config.callback)

            return

        if self.type == "default" and self.config.identifier_position == "append":
            self.result = "http://{}/{}-{}".format(self.config.callback, self.hostname, self.name)

            return

        if self.type == "exec":
            return

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_testname(self, name):
        self.name = name
