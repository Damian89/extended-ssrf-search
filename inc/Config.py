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

import configparser
import os
import sys
from inc.Color import *
from inc.Clean import *


class Config:

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('app-settings.conf')

        self.__set_set_config()

        self.__get_urls()
        self.__get_cookies()
        self.__get_static_headers()

        if self.insertion_point_use_http_headers:
            self.__get_http_headers()

        if self.insertion_point_use_getparams or self.insertion_point_use_postparams or self.insertion_point_use_postparams_as_json:
            self.__get_parameters()

    def __set_set_config(self):

        # Default settings
        self.callback = self.config["default"]["CallbackHost"]
        self.http_method = self.config["default"]["HTTPMethod"]
        self.http_timeout = int(self.config["default"]["HTTPTimeout"])
        self.max_threads = int(self.config["default"]["MaxThreads"])
        self.shuffleTests = self.config.getboolean("default", "ShuffleTests")
        self.sleep_before_testing = int(self.config["default"]["SleepBeforeTesting"])
        self.chunk_size_get = int(self.config["default"]["GetChunkSize"])

        # Settings regarding insertion points
        self.insertion_point_use_path = self.config.getboolean("insertion-points", "InPath")
        self.insertion_point_use_getparams = self.config.getboolean("insertion-points", "InParamsGet")
        self.insertion_point_use_postparams = self.config.getboolean("insertion-points", "InParamsPost")
        self.insertion_point_use_postparams_as_json = self.config.getboolean("insertion-points", "InParamsPostAsJson")
        self.insertion_point_use_http_headers = self.config.getboolean("insertion-points", "InAdditionalHeaders")
        self.insertion_point_use_host = self.config.getboolean("insertion-points", "InHost")

        # Settings regarding attack/payload
        self.attack_use_exec_payload = self.config.getboolean("attacks", "UseExecPayload")
        self.attack_exec_payload = self.config["attacks"]["ExecPayload"]
        self.identifier_position = self.config["identifier"]["Position"]

        # Tunneling
        self.tunneling = self.config.getboolean("tunneling", "Active")
        self.tunnel = self.config["tunneling"]["Tunnel"]

    def __get_cookies(self):

        file = self.config["files"]["Cookies"]

        if not os.path.exists(file):
            sys.exit("Cookie jar not found")

        cookies = open(file, "r").read().splitlines()

        cookies = ";".join([cookie.rstrip() for cookie in cookies if cookie.strip()])

        self.cookies = cookies

    def __get_parameters(self):

        file = self.config["files"]["Parameters"]

        if not os.path.exists(file):
            sys.exit("Param list not found")

        parameters = open(file, "r").read().splitlines()

        parameters = "\n".join([param.rstrip() for param in parameters if param.strip()])

        if len(parameters) == 0:
            sys.exit("Param list seems to be empty")

        self.parameters = parameters

    def __get_http_headers(self):

        file = self.config["files"]["HttpHeaders"]

        if not os.path.exists(file):
            sys.exit("Header list not found")

        headers = open(file, "r").read().splitlines()

        headers = "\n".join([header.rstrip() for header in headers if header.strip()])

        if len(headers) == 0:
            sys.exit("Header list seems to be empty")

        self.headers = headers

    def __get_static_headers(self):

        file = self.config["files"]["StaticHeaders"]

        if not os.path.exists(file):
            sys.exit("Static header list not found")

        static_headers = open(file, "r").read().splitlines()

        static_headers = "\n".join([header.rstrip() for header in static_headers if header.strip()])

        self.static_headers = static_headers

    def __get_urls(self):

        file = self.config["files"]["Urls"]

        if not os.path.exists(file):
            sys.exit("Url list not found")

        urls = open(file, "r").read().splitlines()

        urls = "\n".join([url.rstrip() for url in urls if url.strip()])

        if len(urls) == 0:
            sys.exit("Url list seems to be empty!")

        urls = urls.splitlines()

        self.original_url_count = len(urls)

        url_cleaner = Clean(urls)
        url_cleaner.clean()
        self.urls = url_cleaner.cleaned_urls
        self.cleaned_url_count = len(self.urls)

    def show_summary(self):

        if self.identifier_position == "prepend":
            print("{} Callback:\t\t\t%host%.{}".format(Color.orange("[ i ]"), self.callback))
        else:
            print("{} Callback:\t\t\t{}/%host%".format(Color.orange("[ i ]"), self.callback))

        print("{} HTTP Method:\t\t{}".format(Color.orange("[ i ]"), self.http_method))
        print("{} Threads:\t\t\t{}".format(Color.orange("[ i ]"), self.max_threads))
        print("{} HTTP Timeout:\t\t{}".format(Color.orange("[ i ]"), self.http_timeout))

        methods = []

        if self.insertion_point_use_path:
            methods.append("path")

        if self.insertion_point_use_host:
            methods.append("host")

        if self.insertion_point_use_http_headers:
            methods.append("headers")

        if self.insertion_point_use_getparams:
            methods.append("get-parameters")

        if self.insertion_point_use_postparams:
            methods.append("form-post-parameters")

        if self.insertion_point_use_postparams_as_json:
            methods.append("json-post-parameters")

        print("{} Insertion points:\t\t{}".format(
            Color.orange("[ i ]"),
            ", ".join(methods)
        ))

        if self.tunneling:
            print("{} Proxy server:\t\t{}".format(
                Color.orange("[ i ]"),
                self.tunnel
            ))

        if self.attack_use_exec_payload:
            print("{} OS command payload:\t{}".format(Color.orange("[ i ]"), self.attack_exec_payload))

        if self.cookies.strip() != "":
            print("{} Cookies used:\t\t{}".format(Color.orange("[ i ]"), self.cookies.strip()))

        if self.insertion_point_use_http_headers and self.headers.strip() != "":
            print("{} Testable headers:\t\t{}".format(
                Color.orange("[ i ]"),
                ", ".join([header for header in self.headers.splitlines()])
            ))

        if self.static_headers.strip() != "":
            print("{} Static headers:\t\t{}".format(
                Color.orange("[ i ]"),
                ", ".join([header for header in self.static_headers.splitlines()])
            ))

        print("{} Initial url count:\t{}".format(
            Color.orange("[ i ]"),
            self.original_url_count
        ))

        print("{} Cleaned url count:\t{}".format(
            Color.orange("[ i ]"),
            self.cleaned_url_count
        ))
