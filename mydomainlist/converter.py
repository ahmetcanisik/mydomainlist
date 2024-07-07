#!/usr/bin/env python3
import whois
import json
from utils import log
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

stat = {
    "purchased": 0,
    "available": 0
}

def available_domain(domain):
    try:
        w = whois.whois(domain)
        log(message=f"domain : {w}")
        return w.domain_name is not None and len(w.domain_name) > 0
    except Exception as e:
        log(type="err", message="error " + str(e))
        return False


def check_domain(domain):
    log(message=f"aktifliği kontrol ediliyor... {domain['Domain']}")
    if (available_domain(domain['Domain'])):
        status = "❌ purchased"
        stat["purchased"] += 1
    else:
        status = "✅ available"
        stat["available"] += 1
    log(type="good", message=f"kontrol tamamlandı: {domain['Domain']} şu anda {status}")
    return domain['Domain'], domain['Description'], status


def ConvertMarkdown(domains_path, title, readme, domain_check):
    with open(domains_path, "r", encoding="utf-8") as domains_file:
        domain_list = json.load(domains_file)

    markdown = ""
    for category, domains in domain_list.items():
        markdown += f"## {category.title().replace('_', ' ')}\n"

        if domain_check:
            markdown += "| Domain Name | Description | Status |\n"
            markdown += "|-------------|-------------|--------|\n"

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(check_domain, domain): domain for domain in domains}
                for future in as_completed(futures):
                    domain, description, status = future.result()
                    markdown += f"| <a href=\"https://whois.com/whois/{domain}\" target=\"_blank\">{domain}</a> | {description} | {status} |\n"

        else:
            markdown += "| Domain Name | Description \n"
            markdown += "|-------------|-------------\n"

            for domain in domains:
                markdown += f"| <a href=\"https://whois.com/whois/{domain['Domain']}\" target=\"_blank\">{domain['Domain']}</a> | {domain['Description']}\n"
    
    markdown += "\n<br /><br />\n"
    markdown += "\n\nLICENSE: [MIT](LICENSE)"
    
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    final_version = f"# {title}\n\n"
    final_version += f"""> [!NOTE]  
> ⌚ The activity status of domain names was last checked on: `{date}`   
> ❌ Purchased Domains : `{stat["purchased"]}`    
> ✅ Available Domains : `{stat["available"]}`\n\n"""
    final_version += f"""> [!TIP]  
> You can check out the notes for future releases [here](notes.md).\n\n"""
    final_version += f"## Categories\n\n"
    for cat in domain_list.keys():
        link = cat.lower().replace('_', '-')
        final_version += f"- [{cat.title().replace('_', ' ')}](#{link})\n"
    
    final_version += "<br /><br />\n"
    final_version += markdown
    with open(readme, 'w', encoding="utf-8") as file:
        file.write(final_version)