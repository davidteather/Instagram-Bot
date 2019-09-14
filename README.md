# Instagram-Bot

This is an instagram bot that was developed to follow, like, and comment on different instagram posts. This was a comissioned project I developed. With this project you will be able to easily auto assign proxies to different instagram accounts, create jobs for instagram accounts to gain a specific number of likes/follows/comments.

## Getting Started

The following instructions will help you get you running this software.

### Prerequisites

To install the python requirements please run the command below.

```
pip install -r requirements.txt
```

### Installing

You need to have firefox installed. Download [here](https://www.mozilla.org/en-US/firefox/new/)

### Linux
```
sudo apt install firefox
```

You also need to download geckodriver and include it in your path. Download it [here](https://github.com/mozilla/geckodriver/releases)

### Linux
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz 
tar -C /opt -xzf /tmp/geckodriver.tar.gz 
sudo chmod 755 /opt/geckodriver 
sudo ln -fs /opt/geckodriver /usr/bin/geckodriver 
sudo ln -fs /opt/geckodriver /usr/local/bin/geckodriver
```

or the combined command
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && tar -C /opt -xzf /tmp/geckodriver.tar.gz && sudo chmod 755 /opt/geckodriver && sudo ln -fs /opt/geckodriver /usr/bin/geckodriver && sudo ln -fs /opt/geckodriver /usr/local/bin/geckodriver
```

### Windows

First download the geckodriver [here](https://github.com/mozilla/geckodriver/releases), tested with version v0.24.0

Then add geckodriver to your path [here's](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/) a tutorial on how to do that.

## Running the program

To run the software you first need to add information into the inputs/accounts.json, inputs/proxies.json, jobs.json, and settings.json.
Examples of these files are below.

### **Example inputs/acounts.json**
```
[{
        "username": "instagramUsername",
        "password": "instagramPassword",
        "defaultComment": "defaultMessageThisAccountComments"
    },
    {
        "username": "instagramUsername2",
        "password": "instagramPassword2",
        "defaultComment": "defaultMessageThisAccountComments2"
    }
]
```

**username** - This is where the instagram account's username goes.

**password** - This is where the instagram account's password goes.

**defaultComment** - This is what the default comment string will be for the instagram comments. Comment order is defaultComment + globalCommentString (mentioned later)

### **Example of inputs/proxies.json**
```
[{
        "proxy-address": "xx.xxx.xxx.xxxx",
        "proxy-port": "xxxx"
    },
    {
        "proxy-address": "xx.xxx.xxx.xxxx",
        "proxy-port": "xxxx"
    }
]
```

**proxy-address** - This is the proxy IP that you want to be auto assigned to the new accounts in inputs/accounts.json.

**proxy-port** - This is where the proxy port goes for the proxy server

**Note** - It seems that the proxy servers work with only https servers.

### **Example of settings.json**
```
{
    "globalCommentString": "End_Of_Every_Comment",
    "headless": "False"
}
```

**globalCommentString** - This is the variable that will be added onto EVERY comment by any account at the end.

**headless** - Either True or False, tells the browser to do either headless or not. Default is False, because at least for chrome you can [detect chrome headless browsers](https://antoinevastel.com/bot%20detection/2017/08/05/detect-chrome-headless.html)

### **Example of jobs.json**
```
[
    {
        "url": "https://www.instagram.com/github/",
        "amount_of_followers_to_gain": "1"
    },
    {
        "url": "https://www.instagram.com/p/BvzWaX8hg50/",
        "amount_of_likes_to_gain": "1",
        "amount_of_comments_to_gain": "1"
    }
]
```

**url** - Either a link to a specific user or a post. With a post you can specifiy like/comment, with an account you can follow as well.

**amount_of_followers_to_gain** - The amount of followers you want that account to gain.

**amount_of_likes_to_gain** - The amount of likes you want a post to gain.

**amount_of_comments_to_gain** - The amount of comments you want a given post to gain.

**Note** - Make sure you have enough accounts in data/pairedAccounts.json to handle the amount of followers/likes/comments to gain. It is limited to 1 per user.

Once you have all of the json files configured as you would like simpily run the command below.
```
python main.py
```

Then the bot will auto assign new accounts and proxies to eachother adding them to data/pairedAccounts.json and removing them from the input json files. 

After that the bot will then log into accounts in random orders and complete the jobs.

## Built With

* [Python 3.7](https://www.python.org/) - The language used

## Authors

* **David Teather** - *Initial work* - [davidteather](https://github.com/davidteather)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
