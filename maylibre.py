# -*- coding: utf-8 -*-

"""
Copyright 2020 tudstlennkozh

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import smtpd
import email
import email.header
import getpass
import asyncore
import configparser

from datetime import datetime
from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, OAuth2Credentials, \
    OAuth2AuthorizationCodeCredentials, FaultTolerance, Configuration, NTLM, GSSAPI, SSPI, \
    OAUTH2, Build, Version, Message, Mailbox, FileAttachment, HTMLBody
from exchangelib.autodiscover import AutodiscoverProtocol


__version__ = '0.0.5'


def is_probably_html(_s: str, content_type: str) -> bool:
    if content_type.lower() == "text/html":
        return True
    return False


def decode_mime_words(s):
    """
    will handle 's' even if still mime encoded and return a correct string

    >>> decode_mime_words('àç_(àçyfhzeiçà"')
    'àç_(àçyfhzeiçà"'
    >>> decode_mime_words('=?utf-8?b?w6DDp18oJ8Ogw6d5Zmh6ZWnDp8OgJw==?=')
    "àç_('àçyfhzeiçà'"
    """
    return u''.join(
        word if isinstance(word, str) else word.decode(encoding or 'utf8')
            for word, encoding in email.header.decode_header(s))


class CustomSMTPServer(smtpd.SMTPServer):

    no = 0

    def __init__(self, localaddr, account, directory_for_eml=None):
        super().__init__(localaddr, None)
        self.account = account
        if directory_for_eml:
            self.local_copy_emails = True
            self.directory_for_eml = directory_for_eml
        else:
            self.local_copy_emails = False

    def _save_message(self, data):
        if self.local_copy_emails:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.no}.eml"
            with open(os.path.join(self.directory_for_eml, filename), 'wb') as f:
                f.write(data)
            print(f"{filename} saved.")
        self.no += 1

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))

        self._save_message(data)

        msg = email.message_from_bytes(data)

        if msg.is_multipart():
            print("multipart mail, ignored!")
        else:
            subject = decode_mime_words(msg.get('subject', ''))
            body = msg.get_payload(decode=True).decode('utf8')
            charset = msg.get_content_charset()
            content_encoding = msg.get('content-transfer-encoding', '')
            content_type = msg.get_content_type()

            print('Message subject       :', subject)
            print("orig subject=", msg.get('subject', ''))
            print('Message charset       :', charset)
            print('Message encoding      :', content_encoding)
            print('Message type          :', content_type)

            # now to EWS ...
            if is_probably_html(body, content_type):
                body = HTMLBody(body)

            recipients = [Mailbox(email_address=r) for r in rcpttos]

            m = Message(
                account=self.account,
                folder=self.account.sent,
                subject=subject,
                body=body,
                to_recipients=recipients
            )
            m.send_and_save()
            print("mail sent via Exchange")


def connect(server: str, e_mail: str, username: str, password: str, auth_type=NTLM, access_type=DELEGATE) -> Account:
    """
    Get Exchange account connection with server
    """
    creds = Credentials(username=username, password=password)
    config = Configuration(server=server, credentials=creds, auth_type=auth_type)
    return Account(primary_smtp_address=e_mail, autodiscover=True,
                   config=config, credentials=creds, access_type=access_type)


def display_account_infos(account) -> None:
    """
    Display some stats about this account
    (suppose account is a valid live object)
    """
    print(account.mail_tips)
    i = account.inbox
    print(i.all())
    print("global stats for inbox:")
    for attr in ['total_count', 'unread_count']:
        print("%s:%s" % (attr, getattr(i, attr)))


def run(server: str, e_mail: str, username: str, password: str, port, directory_for_eml) -> None:
    print(f"connecting to {server} ...")
    account = connect(server, e_mail, username, password)

    display_account_infos(account)
    account.root.refresh()

    s = CustomSMTPServer(('localhost', port), account, directory_for_eml)
    print(f"listening on port {s.addr[1]} ...")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("Interrupted !")
        pass


CONFIG_FILENAME='maylibre.cfg'
SECTION        ='DEFAULT'
S_SERVER       = 'server'
S_EMAIL        = 'email'
S_USER         = 'username'
S_LOCALCOPY    = 'eml_directory'
config_values= {
    S_SERVER:    'mail server name',
    S_EMAIL:     'email address for account',
    S_USER:      'like DOMAIN\\login',
    S_LOCALCOPY: 'dir where to put .eml of emails sent, leave empty if you don\'t want a local copy'}


def ask_for_config(config_filename: str, config: configparser) -> None:
    print('no config file, please fill in missing values')
    for v, tip in config_values.items():
        config.set(SECTION, v, input(f"{v}({tip}):"))

    with open(config_filename, 'w') as configfile:
        config.write(configfile)
    print(f"configuration saved in {os.path.realpath(configfile.name)}")


def main() -> None:
    """
    main function.
    checks if cfg file exists, creates if needed and then run a local smtp server.
    """
    print(f'mayLibre {__version__}')
    # just try to read config file
    config = configparser.RawConfigParser()
    try:
        with open(CONFIG_FILENAME) as f:
            config.read_file(f)
    except IOError:
        # not here ? so please give parameters ...
        ask_for_config(CONFIG_FILENAME, config)
    # Connection details
    server: str = config.get(SECTION, S_SERVER)
    e_mail: str = config.get(SECTION, S_EMAIL)
    username: str = config.get(SECTION, S_USER)
    local_copy: str = config.get(SECTION, S_LOCALCOPY)
    password = getpass.getpass(f"Password for {username}:")

    run(server, e_mail, username, password, 1025, local_copy)


if __name__ == '__main__':
    main()
