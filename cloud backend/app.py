import whois
from datetime import datetime, timedelta

def check_domain_age(domain_name):
    try:
        # 1. Fetch domain registration data
        w = whois.whois(domain_name)
        
        # 2. Get the creation date (sometimes it's a list, so we take the first)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if not creation_date:
            return "Unknown"

        # 3. Logic: Is it less than 24 hours old?
        now = datetime.now()
        is_new = now - creation_date < timedelta(hours=24)
        
        return is_new # Returns True if it's a "burner" site
    except:
        return True # If it fails, assume it's suspicious