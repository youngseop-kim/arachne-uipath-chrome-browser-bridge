# arachne-uipath chrome browser bridge
> **author** : youngseop-kim <br>
> **project** : arachne-uipath

&nbsp; &nbsp; **arachne-uipath chrome browser bridge** (hereinafter referred to as the bridge) makes the chrome browser enable to communicate with an external application by hosting native messaging pipeline. as the chrome extension only takes the part of scripting and returing results, please make sure that it does not provide any functionality without the host application which is also known as "native application" described in the official document for chrome extension. you may create your own native application which of name is "com.arachne.uipath.chrome.browser.bridge.host" and allowed to accept stdio, or you may use the native application uploaded in this respository. 

&nbsp; &nbsp; finally, we have one thing left before using the bridge. although a decision where a port from the host application opens depends on users, we strongly recommend the communication with an external application should be opened in a localhost, not in public. even if you have to open your port in public, you should aware that it is very dangerous behavior for the security. it does not support any encryption for messages because it is not considered any functionality for the public communication, only for the localhost communication from the steps of development.

&nbsp; &nbsp; if you are ready to use the bridge, please follow the steps as below. below steps are based on the host application uploaded in this repository.

**steps**

**1. install the bridge in the chrome browser** : https://chrome.google.com/webstore/detail/arachneuipathchromebrowse/dcgmnehcnnncofekjjoikncbikojekje

**2. install the host configuration file on your registry**

how to install "host.json" on your registry

```console
> cd "move\to\host\app\directory"
> install.bat
```

how to uninstall "host.json" on your registry

```console
> cd "move\to\host\app\directory"
> uninstall.bat
```

**3. install python package for the host application**

how to install chrome native messaging pipeline library from pypi
```console
> pip install cbnmplib
```

**4. restart the chrome browser**

<br> 

## arachne-uipath chrome browser bridge application

> **language** <br>
> &nbsp; &nbsp; - javascript (tested on v8 10.0.139.13) <br>
> 
> **browser** <br> 
> &nbsp; &nbsp; - chrome (tested on v100.0.4896.88 64bit)
> 
> **operating system** <br>
> &nbsp; &nbsp; - windows 10 (tested on v1809 64bit) <br>

**chrome extension**
- id : dcgmnehcnnncofekjjoikncbikojekje
- name : arachne.uipath.chrome.browser.bridge.app
- it is developed in manifest v3 with following permissions described as below, <br> 
"script" : "activeTab", "scripting", "nativeMessaging" <br> 
"host" : "http", "https"

_update as soon as possible..._

<br> 

## arachne-uipath chrome browser bridge host
> **language** <br> 
> &nbsp; &nbsp; - python (tested on v3.9.0 64bit) <br>
> 
> **operating system** <br>
> &nbsp; &nbsp; - windows 10 (tested on v1809 64bit) <br>

_update as soon as possible..._

<br>

## arachne-uipath chrome browser bridge client
> **language** <br> 
> &nbsp; &nbsp; - python (tested on v3.9.0 64bit) <br>
> 
> **operating system** <br>
> &nbsp; &nbsp; - windows 10 (tested on v1809 64bit) <br>

_update as soon as possible..._

<br>

## chrome browser native messaging pipeline library
> **language** <br> 
> &nbsp; &nbsp; - python (tested on v3.9.0 64bit) <br>
> 
> **operating system** <br>
> &nbsp; &nbsp; - windows 10 (tested on v1809 64bit) <br>

_update as soon as possible..._

<br>

