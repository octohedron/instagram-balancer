# Instagram balancer

Unfollows anyone that doesn't follow you back, most of them are bots anyways.

It uses selenium to get all the information so install it with:
```bash
pip install selenium
```

Install the proper `chromedriver` for your operating system.  Once you (download it)[https://sites.google.com/a/chromium.org/chromedriver/downloads] just drag and drop it into the `instagram-profilecrawl` directory.

## Use it!

```bash
$ export INSTA_PW=your_password
$ export INSTA_USER=your_user
$ python3 unfollow_nonfollowers.py
```

## Example results 