# [nextsms](https://pypi.org/project/nextsms)

[![Downloads](https://pepy.tech/badge/nextsms)](https://pepy.tech/project/nextsms)
[![Downloads](https://pepy.tech/badge/nextsms/month)](https://pepy.tech/project/nextsms)
[![Downloads](https://pepy.tech/badge/nextsms/week)](https://pepy.tech/project/nextsms)

Python Package to easy the integration with nextsms SMS Gateway

[![Become a patron](pictures/become_a_patron_button.png)](https://www.patreon.com/kalebujordan)

Getting started 
---------------

In order to use this package you need to have the NextSMS Account, If you don't have one please take a look at [NextSMS](https://nextsms.co.tz), and get your *username* and *password* we gonna use them down below;

Install the libary from pip or directly

```bash
pip install nextsms
```

Installing directly from github

Clone this repository or Download a zip of the package  and then do this;

```bash
git clone https://github.com/Kalebu/nextsms
cd nextsms 
nextsms -> python setup.py install 
```

Here is an example on how to send an SMS with this package;

```python

>> import nextsms
>> sender = nextsms('your username', 'your password')
>> sender.sendsms(message='hello', recipients=['25575XXXXX','25565XXXX'], sender_id="NEXTSMS")

```

Bulky ?
-------
NextSms allows you to predefine all message you would like to send with variety of sender IDs and does the rest on how to successful send to all.

Here an Example how you would do that with this package

```python

>> import nextsms
>> sender = nextsms('KalebuJordan', 'kalebu@opensource') 
>> messages = [
    {'from':'NEXTSMS', 'to':'255757294146', 'text':'hello'},
    {'from':'NEXTSMS', 'to':'255754205561', 'text':'hello'}]           
>> sender.send_bulk(messages)

```

Environment 
-----------

By default as you can create a nextsms instance it configure the environment to use production urls, If you wanna do on test sandbox here how;

```python

>> import nextsms
>> sender = nextsms('KalebuJordan', 'kalebu@opensource')
>> sender.sandbox = True 

```

Wanna Contribute ?
------------------
Just 
- Fork it 
- Create a new branch 
- Do your changes 
- Make a Pull request
- You're merged congrats .!!!


Give it a star 
--------------

Was this useful to you ? Cool then give it a big star !


Connect with me 
---------------

I use a lot of twitter , [let's connect on twitter](twitter.com/j_kalebu) .


Issues 
------

Encountered issues while using the package, raise an issue and then we gonna work to fix it as soon as it takes

```bash
More features coming soon
```

All the Credits to [kalebu](github.com/kalebu)