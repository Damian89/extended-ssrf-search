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


class Color:

    @staticmethod
    def red(text):
        return "\033[31m{}\033[0m".format(text)

    @staticmethod
    def danger(text):
        return "\033[41m{}\033[94m\033[0m".format(text)

    @staticmethod
    def green(text):
        return "\033[32m{}\033[0m".format(text)

    @staticmethod
    def orange(text):
        return "\033[33m{}\033[0m".format(text)
