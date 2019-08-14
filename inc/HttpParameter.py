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

import json


class HttpParameter:

    def __init__(self, config, oldquery, callback):

        self.config = config
        self.oldquery = oldquery
        self.params = []
        self.finale_query_parts = []
        self.__extract_params_from_query()
        self.__make_combinations(callback)

    def combine_for_get(self):

        query = []

        for data in self.finale_query_parts:
            query.append("{}={}".format(data["param"], data["callback"]))

        return "&".join(query)

    def combine_for_post(self):

        return self.combine_for_get()

    def combine_as_json(self):

        jsonA = {}

        for data in self.finale_query_parts:
            jsonA[data["param"]] = data["callback"]

        return json.dumps(jsonA, ensure_ascii=True)

    def get_data_for_get_in_chunks(self):
        start = 0
        query = []
        chunked = []

        for data in self.finale_query_parts:

            start = start +1

            query.append("{}={}".format(data["param"], data["callback"]))

            if start == self.config.chunk_size_get:
                chunked.append("&".join(query))
                query = []
                start = 0

        if len(query)>0:
            chunked.append("&".join(query))

        return chunked

    def __make_combinations(self, callback):

        for param in self.params:
            self.finale_query_parts.append({
                'param': param,
                'callback': callback
            })

    def __extract_params_from_query(self):

        old_params_exploded = []

        if self.oldquery.strip() != "":
            old_params_exploded = self.oldquery.split("&")

        if len(old_params_exploded) > 0:

            for param_val in old_params_exploded:
                param_name, param_val = param_val.split("=")

                self.params.append(param_name)

        additional_params = self.config.parameters.splitlines()

        for add_param in additional_params:
            self.params.append(add_param)
