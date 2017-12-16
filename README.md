# Instagram balancer

Tired of following bots? Try this awesome tool

Probably works with Python 2, but it's tested on Python 3

It uses selenium, install it with:
```bash
pip3 install selenium
```

Install the proper `chromedriver` for your operating system.  Once you [download it](https://sites.google.com/a/chromium.org/chromedriver/downloads) just drag and drop it into the `instagram-profilecrawl` directory.

## Use it!

```bash
$ export INSTA_PW=your_password
$ export INSTA_USER=your_user
$ python3 unfollow_nonfollowers.py
```

Props to [@timgrossmann](https://github.com/timgrossmann) for inspiration
