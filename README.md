# Python reweet bot (rtbot)

Establishes an API connection to Twitter using Tweepy and retweet tweets based on criteria

## Installation

First, installation of dependencies

```bash
pipenv install
pipenv sync
```

Second, configuration of configuration file, edit `credentials.py`

`vim configuration/credentatials.py `

## Usage

The best is to use a crontab
```bash
0 */2 * * * python3 /home/av1m/rtbot/retweet.py > /dev/null 2>&1
```

We can directly launch it from a terminal (`python3 retweet.py`)

Note that it is possible to use the `Logger` class to retrieve the results by mail/sms/file  

## Author

* [Avi Mimoun](https://www.github.com/av1m)

## Repository available on Github

* [Link of this repository](https://github.com/av1m/rtbot)

## License

* [MIT](https://github.com/av1m/python-retweet/blob/master/LICENSE)