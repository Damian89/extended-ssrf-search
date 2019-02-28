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

import http.client


class Connection:

    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.response = ""

    def connect(self):
        if self.config.tunneling:
            self.__tunneled_connection()
        else:
            self.__regular_connection()

    def __regular_connection(self):

        port = self.__get_port()

        if "https" in self.data["url"]:
            connection = http.client.HTTPSConnection(self.data["host"], port, timeout=self.config.http_timeout)
        else:
            connection = http.client.HTTPConnection(self.data["host"], port, timeout=self.config.http_timeout)

        connection.request(
            self.data["method"].upper(),
            self.data["path"],
            self.data["body"],
            self.data["headers"]
        )

        self.response = connection.getresponse()

        connection.close()

    def __tunneled_connection(self):

        if "https" in self.data["url"]:
            connection = http.client.HTTPSConnection(self.config.tunnel, timeout=self.config.http_timeout)
        else:
            connection = http.client.HTTPConnection(self.config.tunnel, timeout=self.config.http_timeout)

        port = self.__get_port()

        connection.set_tunnel(self.data["host"], port)

        body = self.data["body"]

        if self.data["body"].strip() == "":
            body = None

        connection.request(
            self.data["method"].upper(),
            self.data["path"],
            body,
            self.data["headers"]
        )

        self.response = connection.getresponse()

        connection.close()

    def __get_port(self):
        port = self.data["port"]
        if port is None and "https" in self.data["url"]:
            port = 443
        if port is None and "http" in self.data["url"]:
            port = 80
        return port
