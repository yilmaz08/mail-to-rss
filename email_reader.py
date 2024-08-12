import imaplib
import email
import email.header

def parse_email(res, msg):
    title = "Unknown"
    description = ""
    
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject, encoding = email.header.decode_header(msg.get("Subject"))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding=encoding)

            From, encoding = email.header.decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)

            title = subject
            description += f"From: {From}\n"

            # Parse the content
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        description += body
                    elif "attachment" in content_disposition:
                        description += body + "\nThere are attachments"
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    description += body
            if content_type == "text/html":
                description = "HTML CONTENT" # TODO
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
        title, description = parse_email(res=res, msg=msg)
        emails.append({"title": title, "description": description, "link": "https://github.com/yilmaz08/mail-to-rss"})

    return emails