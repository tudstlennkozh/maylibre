<h2 align="center">
    MayLibre
</h2>
<h3 align="center">
    Eases mailing from LibreOffice to an Exchange server
</h3>
<h4 align="center">
  <a href="#description">Description</a> |
  <a href="#installation">Installation</a> |
  <a href="#usage">Usage</a> |
  <a href="#tests">Tests</a> |
  <a href="#licensing">Licensing</a> |
  <a href="#credits">Credits</a> |
  <a href="#release-history">Release History</a>
</h4>

## Description

If you ever wanted to :

* send mass mailing from [LibreOffice](https://www.libreoffice.org/)
* not setup a smtp server
* rely on [Exchange Web Server](https://en.wikipedia.org/wiki/Microsoft_Exchange_Server)

this script is made for you !

![screenshot](media/screenshot.png)

This script runs as a local smtp server, allowing to use mass mailing in LibreOffice, but sends all emails via an Exchange Web Server, just as if you were using it directly from LibreOffice.

Of course, if your server already exposes smtp, you don't need it.

This script does almost nothing, all work is done by the [exchangelib](https://pypi.org/project/exchangelib/) package. This script just glue together a local smtp server and the exchange server.


## Installation

![Python 3.8](https://img.shields.io/badge/python-3.8-blue) 

To install MayLibre, prefer to do so in a virtual environment, then activate it and type the command:

    md maylibre
    cd maylibre
    pip install https://github.com/tudstlennkozh/maylibre/zipball/master

You then have to install needed package :

```
cd 
pip install -r requirements.txt
```

That's it !

## Usage

modify the variables at the begining of the script to suit your EWS account  :

```python
# Connection details
server: str = 'ews.com'
e_mail: str = 'unkwnon@ewsmail.com'
username: str = 'DOMAIN\\login'
```

then :

    python maylibre.py

enter the password associated with the account, and proceed to LibreOffice to send all your emails via your local smtp server directly connected to EWS.

Just type Ctrl+C to end the script when done.

## Tests

This script has been tested on Windows 10, with Python 3.8 and LibreOffice 6.4 on Exchange 2016 server. Please let us know if any other environment is working.

## Licensing

[![Apache 2.0](https://img.shields.io/badge/license-Apache-blue)](/LICENSE)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Credits

Please refer to the included [AUTHORS](/AUTHORS.md) for the full credits. Nothing would have been possible without [exchangelib](https://pypi.org/project/exchangelib/).

## Release History

Please refer to the included [CHANGELOG](/CHANGELOG.md) for the full release
history.

-------------------------
###### © 2020 tudstlennkozh

