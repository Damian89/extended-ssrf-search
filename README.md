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

wip