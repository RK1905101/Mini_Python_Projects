from datetime import datetime

MAIL = "you@example.com"
PASSWORD = "**********"
LOCATIONS = [ #list of locations to target
]

def COVER_LETTER( date: datetime, name: str ) -> str: 
    return f"""
    Your cover letter content here with date: {date.now():%Y-%m-%d}, company name: {name}.
""";