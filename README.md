# Python reweet bot (rtbot)

[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/av1m/python-retweet/?ref=repository-badge)
[![CodeInspector Score](https://www.code-inspector.com/project/5622/score/svg)](https://frontend.code-inspector.com/public/project/5622/python-retweet/dashboard)
[![CodeInspector Status](https://www.code-inspector.com/project/5622/status/svg)](https://frontend.code-inspector.com/public/project/5622/python-retweet/dashboard)

Establishes an API connection to Twitter using Tweepy and retweet tweets based on criteria

## Installation

First, installation of dependencies

```bash
python3 -m pip install -r requirements.txt
```

Second, configuration of configuration file, edit `credentials.py`

`vim configuration/credentatials.py `

## Usage

The best is to use a crontab
```bash
0 */2 * * * python3 /home/av1m/rtbot/retweet.py > /dev/null 2>&1
```

We can directly launch it from a terminal (`python3 retweet.py`)

Note that it is possible to use the [`Logger`](include/logger.py) class to retrieve the results by mail/sms/file  

## TODO

See the [Projects section](https://github.com/av1m/python-retweet/projects) on Github

## Author

* [Avi Mimoun](https://www.github.com/av1m)

## Repository available on Github

* [Link of this repository](https://github.com/av1m/rtbot)

## License

* [MIT](https://github.com/av1m/python-retweet/blob/master/LICENSE)

### Useful links

- https://developer.twitter.com/en/docs/basics/rate-limiting
- http://docs.tweepy.org/en/v3.5.0/api.html
- https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
- https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets