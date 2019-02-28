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
from urllib.parse import urlparse


class Clean:

    def __init__(self, urls):
        self.urls = urls
        self.cleaned_urls = []
        self.new_list = []

    def clean(self):

        self.__make_initial_urls_unique()

        for url in self.urls:
            h, p, po, q, s = self.__get_url_parts(url)

            params = self.__extract_params(q)

            new_url = self.__create_base_url_string(h, p, po, s)

            param_string = self.__create_sorted_param_string(params)

            new_url = self.__append_param_string(new_url, param_string)

            new_url = self.__remove_last_char_if_its_ampersand(new_url)

            self.new_list.append(new_url)

        self.__make_new_url_list_unique()

        self.cleaned_urls = self.new_list

    def __make_new_url_list_unique(self):
        self.new_list = list(set(self.new_list))

    def __remove_last_char_if_its_ampersand(self, new_url):

        new_url = new_url.rstrip("&")

        return new_url

    def __append_param_string(self, new_url, param_string):

        if param_string != "":
            new_url = "{}?{}".format(new_url, param_string)

        return new_url

    def __create_base_url_string(self, h, p, po, s):

        new_url = "{}://{}".format(s, h)

        if po is not None:
            new_url = "{}:{}".format(new_url, po)

        if p == "":
            p = "/"

        new_url = "{}{}".format(new_url, p)

        return new_url

    def __create_sorted_param_string(self, params):

        param_string = ""

        for value, param in enumerate(params):
            param_string = "{}{}={}&".format(param_string, param, value)

        return param_string

    def __extract_params(self, q):

        params = []

        if q is not "":

            for element in q.split("&"):
                params.append(element.split("=")[0])

        params.sort()

        return params

    def __get_url_parts(self, url):

        u = urlparse(url)

        s = u.scheme

        h = u.hostname

        po = u.port

        p = u.path

        q = u.query

        return h, p, po, q, s

    def __make_initial_urls_unique(self):
        self.urls = list(set(self.urls))
