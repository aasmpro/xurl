### xurl

extract links (href data) from html files/web pages.

#### Installation
```
pip install xurl
```

#### Options
run the `xurl -h` or `xurl --help` for options
```
-a = append an URL to start of the links
-c = contain text (REGEX)
-C = not contain text (REGEX)
-q = quiet mode (do not print Errors/Warnings/Infos)
-v = version
```

#### Usages
```
xurl https://example.com
```
and same for the files
```
xurl path/to/file
```
search using regex
```
xurl https://example.com -c "section\-[1-10].*.[pdf|xlsx]"
```