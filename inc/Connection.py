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

        if "https" in self.data["url"]:
            connection = http.client.HTTPSConnection(self.data["host"], 443, timeout=self.config.http_timeout)
        else:
            connection = http.client.HTTPConnection(self.data["host"], 80, timeout=self.config.http_timeout)

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

        if "https" in self.data["url"]:
            connection.set_tunnel(self.data["host"], 443)
        else:
            connection.set_tunnel(self.data["host"])

        connection.request(
            self.data["method"].upper(),
            self.data["path"],
            self.data["body"],
            self.data["headers"]
        )

        self.response = connection.getresponse()

        connection.close()
