import requests

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    'referer': "https://www.urbancompany.com/robots.txt"
}

url = 'https://www.urbancompany.com/services/sitemap.xml'
r = requests.get(url, headers=headers)

open('sitemap.xml', 'wb').write(r.content)
