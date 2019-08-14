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

from inc.Callback import *
from inc.Headers import *
from inc.HttpParameter import *
from inc.Color import *
from random import shuffle


class Tests:

    def __init__(self, config):

        self.config = config
        self.tests = []
        self.path_tested_hosts = []
        self.host_tested_hosts = []

        self.__create_tests()

    def __create_tests(self):

        for attacked_site in self.config.urls:

            url = self.__make_url(attacked_site)
            path = self.__get_path(url)
            query = self.__get_query(url)
            hostname = self.__get_host(url)
            port = self.__get_port(url)

            if self.config.insertion_point_use_path and hostname not in self.path_tested_hosts:
                self.__create_path_testcase(url, hostname, port)

                self.path_tested_hosts.append(hostname)

            if self.config.insertion_point_use_host and hostname not in self.host_tested_hosts:
                self.__create_host_testcase(url, hostname, port, path, query)

                self.host_tested_hosts.append(hostname)

            if self.config.insertion_point_use_http_headers:
                self.__create_http_header_testcases(url, hostname, port, path, query)

            if self.config.insertion_point_use_getparams:
                self.__create_getparams_testcase(url, hostname, port, path, query)

            if self.config.insertion_point_use_postparams:
                self.__create_postparams_testcase(url, hostname, port, path, query)

            if self.config.insertion_point_use_postparams_as_json:
                self.__create_postparams_json_testcase(url, hostname, port, path, query)

        if self.config.shuffleTests:
            shuffle(self.tests)

        print("{} Request count:\t\t{}".format(
            Color.orange("[ i ]"),
            len(self.tests)
        ))
        print("")

    def __create_postparams_json_testcase(self, url, hostname, port, path, query):

        real_path = "{}?{}".format(path, query)

        if query == "":
            real_path = "{}".format(path)

        callback = Callback(url, self.config, "dns", "default")
        callback.set_hostname(hostname)
        callback.set_testname("jpdd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "application/json")

        params = HttpParameter(self.config, query, callback.result)

        self.tests.append({
            'url': url,
            'port': port,
            'method': 'POST',
            'host': hostname,
            'path': real_path,
            'headers': headers.make(),
            'body': params.combine_as_json(),
            'test_name': "json_post_dns_default"
        })

        callback = Callback(url, self.config, "http", "default")
        callback.set_hostname(hostname)
        callback.set_testname("jphd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "application/json")

        params = HttpParameter(self.config, query, callback.result)

        self.tests.append({
            'url': url,
            'port': port,
            'method': 'POST',
            'host': hostname,
            'path': real_path,
            'headers': headers.make(),
            'body': params.combine_as_json(),
            'test_name': "json_post_http_default"
        })

    def __create_postparams_testcase(self, url, hostname, port, path, query):

        callback = Callback(url, self.config, "dns", "default")
        callback.set_hostname(hostname)
        callback.set_testname("pdd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "application/x-www-form-urlencoded")

        params = HttpParameter(self.config, query, callback.result)

        self.tests.append({
            'url': url,
            'port': port,
            'method': 'POST',
            'host': hostname,
            'path': "{}?{}".format(path, query),
            'headers': headers.make(),
            'body': params.combine_for_post(),
            'test_name': "post_dns_default"
        })

        callback = Callback(url, self.config, "http", "default")
        callback.set_hostname(hostname)
        callback.set_testname("pohd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "application/x-www-form-urlencoded")

        params = HttpParameter(self.config, query, callback.result)

        self.tests.append({
            'url': url,
            'port': port,
            'method': 'POST',
            'host': hostname,
            'path': "{}?{}".format(path, query),
            'headers': headers.make(),
            'body': params.combine_for_post(),
            'test_name': "post_http_default"
        })

    def __create_getparams_testcase(self, url, hostname, port, path, query):

        callback = Callback(url, self.config, "dns", "default")
        callback.set_hostname(hostname)
        callback.set_testname("gdd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")

        params = HttpParameter(self.config, query, callback.result)

        for paramset in params.get_data_for_get_in_chunks():
            self.tests.append({
                'url': url,
                'port': port,
                'method': 'GET',
                'host': hostname,
                'path': "{}?{}".format(path, paramset),
                'headers': headers.make(),
                'body': '',
                'test_name': "get_dns_default"
            })


        callback = Callback(url, self.config, "http", "default")
        callback.set_hostname(hostname)
        callback.set_testname("ghd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")

        params = HttpParameter(self.config, query, callback.result)

        for paramset in params.get_data_for_get_in_chunks():
            self.tests.append({
                'url': url,
                'port': port,
                'method': 'GET',
                'host': hostname,
                'path': "{}?{}".format(path, paramset),
                'headers': headers.make(),
                'body': '',
                'test_name': "get_http_default"
            })

    def __create_http_header_testcases(self, url, hostname, port, path, query):

        callback = Callback(url, self.config, "dns", "default")
        callback.set_hostname(hostname)
        callback.set_testname("hedd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}{}?{}".format(url, path, query))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")
        headers.add_user_defined_headers(callback.result)

        self.tests.append({
            'url': url,
            'port': port,
            'method': self.config.http_method,
            'host': hostname,
            'path': "{}?{}".format(path, query),
            'headers': headers.make(),
            'body': '',
            'test_name': "headers_dns_default"
        })

        callback = Callback(url, self.config, "http", "default")
        callback.set_hostname(hostname)
        callback.set_testname("hthd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}{}?{}".format(url, path, query))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")
        headers.add_user_defined_headers(callback.result)

        self.tests.append({
            'url': url,
            'port': port,
            'method': self.config.http_method,
            'host': hostname,
            'path': "{}?{}".format(path, query),
            'headers': headers.make(),
            'body': '',
            'test_name': "headers_http_default"
        })

        if self.config.attack_use_exec_payload:
            callback = Callback(url, self.config, "dns", "exec")
            callback.set_hostname(hostname)
            callback.set_testname("hede")
            callback.make()

            headers = Headers(self.config)
            headers.set("Host", hostname)
            headers.add_static_headers()
            headers.set("Cookie", self.config.cookies)
            headers.set("Referer", "{}{}?{}".format(url, path, query))
            headers.set("User-Agent", headers.get_random_user_agent())
            headers.set("Content-Type", "text/html")
            headers.add_user_defined_headers(callback.result)

            self.tests.append({
                'url': url,
                'port': port,
                'method': self.config.http_method,
                'host': hostname,
                'path': "{}?{}".format(path, query),
                'headers': headers.make(),
                'body': '',
                'test_name': "headers_dns_exec"
            })

    def __create_host_testcase(self, url, hostname, port, path, query):

        callback = Callback(url, self.config, "dns", "default")
        callback.set_hostname(hostname)
        callback.set_testname("hdd")
        callback.make()

        headers = Headers(self.config)
        headers.set("Host", callback.result)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}{}?{}".format(url, path, query))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")

        self.tests.append({
            'url': url,
            'port': port,
            'method': self.config.http_method,
            'host': hostname,
            'path': "{}?{}".format(path, query),
            'headers': headers.make(),
            'body': '',
            'test_name': "host_dns_default"
        })

        if self.config.attack_use_exec_payload:
            callback = Callback(url, self.config, "dns", "exec")
            callback.set_hostname(hostname)
            callback.set_testname("hde")
            callback.make()

            headers = Headers(self.config)
            headers.set("Host", callback.result)
            headers.add_static_headers()
            headers.set("Cookie", self.config.cookies)
            headers.set("Referer", "{}{}?{}".format(url, path, query))
            headers.set("User-Agent", headers.get_random_user_agent())
            headers.set("Content-Type", "text/html")
            headers.set("Host", callback.result)

            self.tests.append({
                'url': url,
                'port': port,
                'method': self.config.http_method,
                'host': hostname,
                'path': "{}?{}".format(path, query),
                'headers': headers.make(),
                'body': '',
                'test_name': "host_dns_exec"
            })

    def __create_path_testcase(self, url, hostname, port):

        callback = Callback(url, self.config, "http", "default")
        callback.set_hostname(hostname)
        callback.set_testname("pahd")
        callback.make()

        headers = Headers(self.config)

        headers.set("Host", callback.result)
        headers.add_static_headers()
        headers.set("Cookie", self.config.cookies)
        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")
        headers.set("Host", hostname)

        self.tests.append({
            'url': url,
            'port': port,
            'method': self.config.http_method,
            'host': hostname,
            'path': callback.result,
            'headers': headers.make(),
            'body': '',
            'test_name': "path_http_default"
        })

    @staticmethod
    def __make_url(attacked_site):

        url = attacked_site

        if not attacked_site.startswith("http"):
            url = "http://{}/".format(attacked_site)

        return url

    @staticmethod
    def __get_path(url):

        parser = urlparse(url)

        path = parser.path

        if path.startswith("http"):
            return path

        if not path.startswith("/"):
            return "/" + path

        return parser.path

    @staticmethod
    def __get_query(url):

        parser = urlparse(url)

        return parser.query

    @staticmethod
    def __get_host(url):

        parser = urlparse(url)

        return parser.hostname

    @staticmethod
    def __get_port(url):

        parser = urlparse(url)

        return parser.port
