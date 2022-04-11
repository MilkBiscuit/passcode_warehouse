# Why making this program

![Password Rules](https://pbs.twimg.com/media/CMKb_QvUAAAZ2vH?format=png&name=small)

I'm pretty sure this is not new to anyone, you **have to** create different passwords for different websites, plus remembering them - if you ever forget, then you'll have to reset your password. I once input incorrect password 3 times on an online banking website, my account was deactivated, then I **have to** ask other administrators of this business account to help re-activate my account, next I **have to** phone the bank help desk to reset my password.

Sometimes you even forget your username! Is it an email? (Some minority websites do NOT accept email as username indeed.) Is it gmail or hotmail? Or maybe it's actually my mobile number?!

THIS IS SUCH A PAIN!

I am not a fan of LastPass BTW, I'd rather save the password of some rarely-used accounts on cloud notes and then encrypt the note - I can't explain why, I just don't like LastPass.

Chrome and Safari do can help, but which one did you save the password into? Also, as a developer, I have more than 3 Google accounts and more than 3 Apple accounts. What if you want to clear all passwords from your browser?

Just recently, I found it's extremely easy to make a desktop App via Python, so here it is, **Passcode Warehouse**, the local, offline version of LastPass, your passwords are saved on your local machine, not cloud.


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


[//]: # (TODO: Wait for the whole UI complete)

# Read More
[Password rules are bullshit](https://blog.codinghorror.com/password-rules-are-bullshit/)

Thanks to [100 Days of Code](https://www.udemy.com/course/100-days-of-code/) - Day 29
