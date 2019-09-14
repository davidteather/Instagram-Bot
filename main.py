from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Proxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import math
import random
import json
import random
import sys
import emoji


# Initializes the Global Variables in settings.json
with open('settings.json', 'r') as globalVars:
    globalVarJson = json.load(globalVars)

globalCommentString = globalVarJson['globalCommentString']
headless = globalVarJson['headless']


# Function Updates and pairs accounts
def updatePairedAccounts():
    # Loads Arrays
    with open('data/pairedAccounts.json', 'r') as data:
        pairedAccounts = json.load(data)

    with open('inputs/accounts.json', 'r') as data:
        inputAccounts = json.load(data)

    with open('inputs/proxies.json', 'r') as data:
        inputProxies = json.load(data)

    # Adding input users to pairedAccounts.json
    for x in inputAccounts:
        inputAccount = inputAccounts[0]
        newAccount = {
            "username": inputAccount['username'],
            "password": inputAccount['password'],
            "defaultComment": inputAccount['defaultComment']
        }
        pairedAccounts.append(newAccount)
        inputAccounts.remove(inputAccount)

    # Assigning Users Proxies
    for pairedAccount in pairedAccounts:
        if pairedAccount.get('proxy-address') == None:
            while pairedAccount.get('proxy-address') == None:
                # Needs New Proxy
                print(inputProxies)
                try:
                    proxyAddr = inputProxies[0]['proxy-address']
                    proxyPort = inputProxies[0]['proxy-port']
                    proxy = proxyAddr + ":" + proxyPort
                except IndexError:
                    print(
                        "There are not enough proxies to handle the new users. Please add more.")
                    print("Exiting Program")
                    sys.exit(100)

                desired_capability = webdriver.DesiredCapabilities.FIREFOX
                desired_capability['proxy'] = {
                    "proxyType": "manual",
                    "httpProxy": proxy,
                    "ftpProxy": proxy,
                    "sslProxy": proxy
                }
                options = Options()
                if headless == "True" or headless == True:
                    options.headless = True
                # Initializes Driver
                driver = webdriver.Firefox(capabilities=desired_capability, options=options)

                # Makes sure proxy is valid
                validProxy = False
                failedProxy = 0
                if failedProxy <= 5:
                    try:
                        driver.get("https://api.myip.com/")
                        time.sleep(2)
                        
                        ip = json.loads(driver.find_element_by_xpath('//body').text.strip())['ip']
                        print(ip)
                        
                        if str(ip) == proxyAddr:
                            validProxy = True
                    except:
                        failedProxy += 1
                        print("Proxy connection failed, retrying " + str(failedProxy) + "/5")

                driver.quit()

                if validProxy == True:
                    pairedAccount['proxy-address'] = inputProxies[0]['proxy-address']
                    pairedAccount['proxy-port'] = inputProxies[0]['proxy-port']
                    inputProxies.pop(0)
                    
                    break
                else:
                    print(proxyAddr + " is not a valid proxy, removing from list.")
                    inputProxies.pop(0)
                    continue

        # Rewrites arrays to the files
        with open('data/pairedAccounts.json', 'w') as data:
            data.write(json.dumps(pairedAccounts,
                                  indent=4, ensure_ascii=False))

        with open('inputs/accounts.json', 'w') as data:
            data.write(json.dumps(inputAccounts, indent=4, ensure_ascii=False))

        with open('inputs/proxies.json', 'w') as data:
            data.write(json.dumps(inputProxies, indent=4, ensure_ascii=False))


# Function to follow a user
def followUser(pairedAccounts, job, usedAccounts, availableAccounts, follows, followsNeeded, followedUserAccounts):
    if follows < followsNeeded:
        # Gets random user
        index = random.randint(0, availableAccounts)
        username = pairedAccounts[index]['username']
        # Makes sure it's not already used
        if username not in usedAccounts:
            proxyADDR = pairedAccounts[index]['proxy-address'] + \
                ":" + pairedAccounts[index]['proxy-port']
            print(proxyADDR)

            desired_capability = webdriver.DesiredCapabilities.FIREFOX
            desired_capability['proxy'] = {
                "proxyType": "manual",
                "httpProxy": proxyADDR,
                "ftpProxy": proxyADDR,
                "sslProxy": proxyADDR
            }

            options = Options()
            if headless == "True" or headless == True:
                options.headless = True

            driver = webdriver.Firefox(capabilities=desired_capability, options=options)
            # Tests proxy
            validProxy = False
            failedProxy = 0
            while True:
                if failedProxy <= 5:
                    try:
                        driver.get("https://api.myip.com/")
                        time.sleep(2)

                        ip = json.loads(driver.find_element_by_xpath(
                            '//body').text.strip())['ip']
                        print(ip)

                        if str(ip) == pairedAccounts[index]['proxy-address']:
                            validProxy = True
                        False
                        break

                    except:
                        print("Invalid PROXY setup")
                        failedProxy += 1
                else:
                    print("Proxy Failed 5 times")
                    sys.exit(101)

            if validProxy == True:
                while True:
                    try:
                        driver.get("https://www.instagram.com/accounts/login/")

                        break
                    except:
                        print("Instagram Timed Out, retrying")

                while True:
                    try:
                        time.sleep(random.uniform(0, 3))
                        driver.find_element_by_xpath(
                            "//input[@name='username']").send_keys(pairedAccounts[index]['username'])
                        time.sleep(random.uniform(0, 3))
                        driver.find_element_by_xpath(
                            "//input[@name='password']").send_keys(pairedAccounts[index]['password'])
                        time.sleep(random.uniform(0, 2))
                        driver.find_element_by_xpath(
                            "//button[@type='submit']").click()
                        time.sleep(5)
                        driver.get('https://www.instagram.com/' +
                                pairedAccounts[index]['username'].lower() + '/')
                        time.sleep(5)
                        driver.find_element_by_xpath(
                            '//span[@aria-label="Options"]')
                        break
                    except:
                        continue

                while True:
                    try:
                        driver.get(job.get('url'))
                        time.sleep(random.uniform(3, 6))

                        driver.find_elements_by_xpath('//button')[0].click()
                        time.sleep(random.uniform(3, 7))
                        followed = True

                        break
                    except:
                        print("Instagram Timed Out thingggy")

                if followed == True:
                    followedUserAccounts.append(username)
                    follows += 1

        driver.quit()

    return (pairedAccounts, job, usedAccounts, availableAccounts, follows, followsNeeded, followedUserAccounts)


# This function likes and or comments depending on the job
def likeAndOrComment(pairedAccounts, job, usedAccounts, availableAccounts, commentedNeeded, commentsGiven, usedCommentingAccount, likesGiven):
    # Try to Like Post
    index = random.randint(0, availableAccounts)
    username = pairedAccounts[index]['username']

    if username not in usedAccounts:
        proxyADDR = pairedAccounts[index]['proxy-address'] + \
            ":" + pairedAccounts[index]['proxy-port']
        print(proxyADDR)

        desired_capability = webdriver.DesiredCapabilities.FIREFOX
        desired_capability['proxy'] = {
            "proxyType": "manual",
            "httpProxy": proxyADDR,
            "ftpProxy": proxyADDR,
            "sslProxy": proxyADDR
        }

        options = Options()
        if headless == "True" or headless == True:
            options.headless = True

        driver = webdriver.Firefox(capabilities=desired_capability, options=options)

        validProxy = False
        failedProxy = 0
        while True:
            if failedProxy <= 5:
                try:
                    driver.get("https://api.myip.com/")
                    time.sleep(2)

                    ip = json.loads(driver.find_element_by_xpath(
                        '//body').text.strip())['ip']
                    print(ip)

                    if str(ip) == pairedAccounts[index]['proxy-address']:
                        validProxy = True
                    False
                    break

                except:
                    print("Invalid PROXY setup")
                    failedProxy += 1
            else:
                print("Proxy Failed 5 times")
                sys.exit(101)

        if validProxy == True:
            while True:
                try:
                    driver.get("https://www.instagram.com/accounts/login/")

                    break
                except:
                    print("Instagram Timed Out, retrying")

            while True:
                try:
                    time.sleep(random.uniform(0, 3))
                    driver.find_element_by_xpath(
                        "//input[@name='username']").send_keys(pairedAccounts[index]['username'])
                    time.sleep(random.uniform(0, 3))
                    driver.find_element_by_xpath(
                        "//input[@name='password']").send_keys(pairedAccounts[index]['password'])
                    time.sleep(random.uniform(0, 2))
                    driver.find_element_by_xpath(
                        "//button[@type='submit']").click()
                    time.sleep(5)
                    driver.get('https://www.instagram.com/' +
                               pairedAccounts[index]['username'].lower() + '/')
                    time.sleep(5)
                    driver.find_element_by_xpath(
                        '//span[@aria-label="Options"]')
                    break
                except:
                    continue

            while True:
                try:
                    driver.get(job.get('url'))
                    time.sleep(random.uniform(3, 6))

                    driver.find_elements_by_xpath('//button')[0].click()
                    time.sleep(random.uniform(3, 7))
                    followed = True

                    break
                except:
                    print("Instagram Timed Out thingggy")

            driver.get(job.get('url'))
            time.sleep(5)

            if likesNeeded > likesGiven:
                likedImage = False

                try:
                    driver.find_element_by_xpath(
                        '//span[@aria-label="Like"]').click()
                    likedImage = True
                except:
                    print(
                        "Failed to like, probably already liked image. Finding new accounts")

                if likedImage == True:
                    usedAccounts.append(username)
                    likesGiven += 1

                    if commentedNeeded > commentsGiven:
                        time.sleep(random.randint(0, 5))
                        driver.find_element_by_xpath(
                            '//textarea[@class="Ypffh"]').click()
                        commentString = emoji.emojize(
                            pairedAccounts[index]['defaultComment'], use_aliases=True) + " " + emoji.emojize(globalCommentString, use_aliases=True)
                        # 😂
                        # 🙃
                        # $('textarea').innerHTML = "😂"
                        # .X7cDz/button
                        # $('.X7cDz > button').click()
                        driver.find_element_by_xpath(
                            '//textarea[@class="Ypffh"]').send_keys(commentString)
                        # driver.execute_script('''document.''')
                        time.sleep(random.randint(0, 2))
                        driver.find_element_by_xpath(
                            '//button[@type="submit"]').click()
                        usedCommentingAccount.append(username)
                        commentsGiven += 1

            else:
                if commentedNeeded > commentsGiven:
                    time.sleep(random.randint(0, 5))
                    driver.find_element_by_xpath(
                        '//textarea[@class="Ypffh"]').click()
                    commentString = emoji.emojize(
                        pairedAccounts[index]['defaultComment'], use_aliases=True) + " " + emoji.emojize(globalCommentString, use_aliases=True)
                    # 😂
                    # 🙃
                    # $('textarea').innerHTML = "😂"
                    # .X7cDz/button
                    # $('.X7cDz > button').click()
                    driver.find_element_by_xpath(
                        '//textarea[@class="Ypffh"]').send_keys(commentString)
                    # driver.execute_script('''document.''')
                    time.sleep(random.randint(0, 2))
                    driver.find_element_by_xpath(
                        '//button[@type="submit"]').click()
                    usedCommentingAccount.append(username)
                    commentsGiven += 1

        driver.quit()

    return (usedAccounts, availableAccounts, commentedNeeded, commentsGiven, usedCommentingAccount, likesGiven)
    
# Calls to update account data
updatePairedAccounts()

# Actual Main Handler

# Loads Arrays
with open('data/pairedAccounts.json', 'r') as data:
    pairedAccounts = json.load(data)

with open('inputs/accounts.json', 'r') as data:
    inputAccounts = json.load(data)

with open('inputs/proxies.json', 'r') as data:
    inputProxies = json.load(data)

with open('jobs.json', 'r') as data:
    jobs = json.load(data)
    index = len(jobs)


# Starts iterating over all jobs
for x in range(0, index):
    # Has to be 0 because jobs are destroyed from the list on success
    job = jobs[0]
    if "/p/" in job.get('url'):
        usedAccounts = []
        usedCommentingAccount = []
        availableAccounts = len(pairedAccounts) - 1
        likesNeeded = int(job['amount_of_likes_to_gain'])
        likesGiven = 0
        commentedNeeded = int(job['amount_of_comments_to_gain'])
        commentsGiven = 0
        jobSuccess = False
        if likesNeeded > likesGiven:
            (usedAccounts, availableAccounts, commentedNeeded, commentsGiven, usedCommentingAccount, likesGiven) = likeAndOrComment(
                pairedAccounts, job, usedAccounts, availableAccounts, commentedNeeded, commentsGiven, usedCommentingAccount, likesGiven)
        elif commentedNeeded > commentsGiven:
            (usedAccounts, availableAccounts, commentedNeeded, commentsGiven, usedCommentingAccount, likesGiven) = likeAndOrComment(
                pairedAccounts, job, usedAccounts, availableAccounts, commentedNeeded, commentsGiven, usedCommentingAccount, likesGiven)

        if likesNeeded <= likesGiven and commentedNeeded <= commentsGiven:
            jobs.remove(job)
            jobSuccess = True
        elif commentsGiven >= commentedNeeded:
            jobs.remove(job)
            jobSuccess = True

    else:
        usedAccounts = []
        followedUserAccounts = []
        availableAccounts = len(pairedAccounts) - 1
        followsNeeded = int(job['amount_of_followers_to_gain'])
        follows = 0
        jobSuccess = False
        if follows < followsNeeded:
            (pairedAccounts, job, usedAccounts, availableAccounts, follows, followsNeeded, followedUserAccounts) = followUser(
                pairedAccounts, job, usedAccounts, availableAccounts, follows, followsNeeded, followedUserAccounts)

        if follows >= followsNeeded:
            jobs.remove(job)
            jobSuccess = True


# Rewrites arrays to the json files
with open('jobs.json', 'w') as data:
    data.write(json.dumps(jobs, indent=4, ensure_ascii=False))

with open('data/pairedAccounts.json', 'w') as data:
    data.write(json.dumps(pairedAccounts, indent=4, ensure_ascii=False))

with open('inputs/accounts.json', 'w') as data:
    data.write(json.dumps(inputAccounts, indent=4, ensure_ascii=False))

with open('inputs/proxies.json', 'w') as data:
    data.write(json.dumps(inputProxies, indent=4, ensure_ascii=False))
