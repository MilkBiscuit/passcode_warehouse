# Why making this program

## Forgot your username
Have you ever experienced this frustration: One day you created a new account on Medium just to read a specific article or download a resource file. Several days, weeks, or even months later, you want to log in again. But wait, which email or username did I use to register? Was it my mobile number, Gmail, Hotmail, or even my Apple ID? I can't remember at all, and now I need to check if they provide a 'find username' option.

This happens to the best of us, especially nowadays, when each person would have tens or even hundreds of online accounts.

## Forgot you password
![Password Rules](https://pbs.twimg.com/media/CMKb_QvUAAAZ2vH?format=png&name=small)

I'm sure this is not new to anyone, you **must** create different passwords for different websites, if you ever forgot, then you would have to reset your password.

**THIS IS SUCH A PAIN!**

I am not a fan of LastPass BTW, I'd rather save the password of some rarely-used accounts on cloud notes and then encrypt the note - I can't explain why, I just don't like LastPass, I don't trust it either.

Chrome and Safari do help, but which one did you save the password into? Also, as a developer, I have more than 3 Google accounts and more than 3 Apple accounts, it becomes messy when you save some passwords in this browser and save some others in another browser.

Then I found it's extremely easy to make a desktop App via Python, so here comes a good opportunity to practice, **PasscodeBin**, the local, offline version of LastPass, your passwords are saved on your local machine, not cloud.


# Passcode Warehouse
My goal is to build a self-explanatory GUI, this was as well as I could do it.
## Screenshots
![The Main Screen](https://user-images.githubusercontent.com/20746964/162697575-87caaaee-4ae5-4bb0-8220-b3214a7ebf9b.png)

![The Search Results](https://user-images.githubusercontent.com/20746964/162697564-91105a8b-7e0e-4e2a-9c8f-49b50c1ed128.png)


## Data storage encryption
Passwords will be encrypted before saving into file, here is an example:

```Encrypted JSON
"Amazon": {
    "username": "dc9909@hotmail.com",
    "password": "NeBgRrYW3T2742sCSt8q4QAAJxCAAAAAAGJT6e8sBQivh_S7DIJ29BbyJ1HjTp73Uqy00eWY1c1USrJa3vT3uCWwlI__xoU6QbxYx5o6k9zeAEzImRAeEdshZygK"
}
```

## Download
PasscodeBin for macOS [version 1.4](https://drive.google.com/file/d/1jsW3kC1KSADQb4YESpr-BwYjRb2pKhcI/view), have tested and works fine on macOS Sonoma 14.2.


## How to package a python project
#### Create the setup.py file
py2applet --make-setup launcher.py

### Include resources as data_files in your setup.py
https://stackoverflow.com/a/13146204/4837103

#### Clean up your build directories
rm -rf build dist

#### Development with alias mode
python setup.py py2app -A

#### Run the application
./dist/PasscodeBin.app/Contents/MacOS/PasscodeBin

#### Deploy the App
python setup.py py2app

# Read More
[Password rules are bullshit](https://blog.codinghorror.com/password-rules-are-bullshit/)

Thanks to [100 Days of Code](https://www.udemy.com/course/100-days-of-code/) - Day 29

# Note
If you're using macOS 12 Monterey, please update to Python 3.10.0 or later, otherwise you'll end up seeing a blank window when running.
