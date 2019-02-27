# Extended ssrf search

This tool search for SSRF using predefined settings in different parts of a request (path, host, headers, post and get parameters).

## First step

Rename __example.app-setting.conf__ to __app-setting.conf__ and adjust settings. The most important setting is the callback url. I 
recommend to use burp collaborator.
Then you can add your urls to config/url-to-test.txt. Here the script accepts domains as well as urls with path and queryparameters.
If you like you can add add your own cookies to config/cookie-jar.txt and add additional headers for your requests. The brute force list
which is used in post and get requests is currently small, I dont thing adding 2000 parameters is smart. We should focus on those
which have the highest possibility to be vulnerable. If you don't think so: just add your own!

## Execution

This tool does not expect any argument via CLI, so just type:
```
python3 extended-ssrf-search.py
```

## Configuration

Its possible to set a lot of options and settings, so here are some explanations.

### Files

The main config file is the "app-settings.conf", everything has to be done in that file! Besides that, there are some 
other files which allow to set more complex data like headers, urls and cookies.

__config/cookie-jar.txt__

Use this file to add a cookie string. I usually copy the one which you can see in every burp request. Please just copy the 
value of the "Cookie:"-header. A sample input is in the default file.

__config/http-headers.txt__

This file defines the http headers which are added to the request and manipulated (payload is added to each one). The 
most important ones are already in the file. But feel free to add more.

__config/parameters.txt__

The tool has the option to brute force get and post parameters. In that case those parameters (+ those in the query string)
will be used. Each parameter gets the payload as value. Most important are already in that file.

__config/static-request-headers.txt__

Those headers are added to every request, but they won't get manipulated. They are static. Thats the best place to add 
authorization or bearer cookies. One (Key: Value) per line!

__config/urls-to-test.txt__

Thats the file you need! Please add here your links to scan. The following formats are allowed:

* https://domain.com
* https://domain.com/path
* https://domain.com/path?param=value&param1=value1
* domain.com

When the last case is detected an "http://" is prepended. This tool is intended to work with a good list of urls.
A good way to get one is to just export it using burp. Then you have a valid list of urls. All you need to do ist to just
add your cookies.

### Settings

The app-settings.conf defined the program workflow. Its the most important file, you can activate/deactive different
modules there.

#### Basic settings

__CallbackHost__

The url/host which all dns and http requests are send back - I mostly use burp collaborator here, but DNSBin or you own 
server is also perfect. 

__HTTPMethod__

Defines the request method. Valid options are: GET, POST, PUT, DELETE, PATCH, GET, OPTIONS
Invalid values will produce massiv errors since http.client disallows other methods! I dont check 
if you did something wrong here ;)

__HTTPTimeout__

Some requests can take long. Here you can define the max. execution time of one request. I recommend values
between 2 and 6 seconds.

__MaxThreads__

The more threads, the faster the script is - but since we are dealing with a lot of connections I usually keep this below
10 on my personal computer and arround 30 on my VPS.

__ShuffleTests__

Especially when dealing with a BIG list of urls having this set to "true" will shuffle all created tests. That way the same host 
will not get hit that much. If you scan just one host, than it doesn't matter.


#### Insertion points

Each insertion point can be activated (set to true/1) or deactivated (set to false/0)

__InPath__

The example shows a GET request, but depending on your settings, this could also be
POST, PUT, DELETE, ...

```
GET [INJECT HERE PAYLOAD] HTTP/1.1
...
```

__InHost__

The example shows a GET request, but depending on your settings, this could also be
POST, PUT, DELETE, ...

```
GET /path HTTP/1.1
Host: [INJECT HERE PAYLOAD]
...
```

__InAdditionalHeaders__

The example shows a GET request, but depending on your settings, this could also be
POST, PUT, DELETE, ...

```
GET /path HTTP/1.1
...
X-Forwarded-For: [INJECT HERE PAYLOAD]
```

__InParamsGet__

Here the Method is fixed to GET.

```
GET /path?[INJECT HERE PAYLOAD] HTTP/1.1
...
```

__InParamsPost__

Here the Method is fixed to POST.

```
POST /path HTTP/1.1
...
Content-Type: application/x-www-form-urlencoded
Content-Length: XXX

[INJECT HERE PAYLOAD]
```

__InParamsPostAsJson__

Here the Method is fixed to POST.

```
POST /path HTTP/1.1
...
Content-Type: application/json
Content-Length: XXX

[INJECT HERE JSON-PAYLOAD]
```

#### Attacks

In the default settings this tool just tries to trigger http requests via SSRF. But its also possible to exfiltrate data
using DNS, when an OS command is injected. The most common payload is "$(hostname)". There are some options
which allow to use this kind of attack additionally. 

__UseExecPayload__

Using this setting you can activate/deactivate that behaviour.

__ExecPayload__

Here you can define your own payload, e.g. $(uname -a)

#### Identifier

To make the identification a little bit easier a combination of current host and method (in short form, see Tests.py) is 
appended or prepended to the payload.

__Position__ 

Valid options are "append" and "prepend"!

If "append" is chosen, the payloads look like this:

```
....burpcollaborator.net/www.attacked-domain.com-testmethod
http://....burpcollaborator.net/www.attacked-domain.com-testmethod
```

If "prepend" is chosen, the payloads look like this:

```
www.attacked-domain.com-testmethod.burpcollaborator.net
http://www.attacked-domain.com-testmethod.burpcollaborator.net/
```