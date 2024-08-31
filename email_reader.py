import imaplib
import email
import email.header

def parse_email(res, msg, email_address):
    title = f"Mail for {email_address}"
    description = ""

    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject, encoding = email.header.decode_header(msg.get("Subject"))[0]
            if isinstance(subject, bytes) and encoding is not None:
                title = subject.decode(encoding=encoding)

            From, encoding = email.header.decode_header(msg.get("From"))[0]
            if isinstance(From, bytes) and encoding is not None:
                From = From.decode(encoding=encoding)

            description += f"From: {From}\nTo: {email_address}\n"
    return title, description

def get_emails(email: str, password: str, imap_server: str):
    imap = imaplib.IMAP4_SSL(imap_server)                   # create connection

    try: imap.login(email, password)                        # authenticate
    except: return []                                       # on fail: return empty list # TODO

    status, messages = imap.select("INBOX")                 # get contents of inbox
    message_count = int(messages[0])                        # get message count
    emails = []

    for i in range(message_count):
        res, msg = imap.fetch(str(i+1), "(RFC822)")
        title, description = parse_email(res=res, msg=msg, email_address=email)
        emails.append({"title": title, "description": description, "link": "https://github.com/yilmaz08/mail-to-rss"})

    return emails
