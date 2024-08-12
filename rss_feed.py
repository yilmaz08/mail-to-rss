from feedgen.feed import FeedGenerator

def generate_rss(email: str, emails: list, reverse: bool = False):
    fg = FeedGenerator()
    fg.id(f"https://github.com/yilmaz08/mail-to-rss")
    fg.title(f"{email}")
    fg.link(href=f"https://github.com/yilmaz08/mail-to-rss", rel="alternate")
    fg.description(f"RSS Feed for {email}")

    if reverse:
        emails = emails[::-1]

    for email in emails:
        fe = fg.add_entry()
        fe.id(email["link"])
        fe.title(email["title"])
        fe.description(email["description"])
        fe.link(href=email["link"])

    return fg.rss_str(pretty=True)