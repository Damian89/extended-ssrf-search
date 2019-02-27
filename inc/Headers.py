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


class Headers:

    def __init__(self, config):
        self.config = config
        self.headers = {}

    def add_static_headers(self):
        headers = self.config.static_headers.splitlines()

        for header_string in headers:
            name, value = header_string.split(":")
            self.headers[name] = value.strip()

    def add_user_defined_headers(self, callback):
        headers = self.config.headers.splitlines()

        for header in headers:
            self.headers[header] = callback
            
    def set(self, name, value):
        self.headers[name] = value

    def reset(self):
        self.headers = {}

    def make(self):
        return self.headers
