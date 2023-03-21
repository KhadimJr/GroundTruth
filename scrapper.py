import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

main_url = 'https://mailman.nanog.org/pipermail/nanog/'

keywords = ["Hijacks", "Hijack", "Hijacking", "BGP Hijacking", "Prefix Hijacking"]

# Date ranges (5 years before and after the "serial hijacking studies")

date_range_i = re.compile(r'\bhttps://mailman\.nanog\.org/pipermail/nanog/('
                            r'2009-January|2010-January|2011-January|2012-January|2013-January|'
                            r'2009-February|2010-February|2011-February|2012-February|2013-February|'
                            r'2009-March|2010-March|2011-March|2012-March|2013-March|'
                            r'2009-April|2010-April|2011-April|2012-April|2013-April|'
                            r'2009-May|2010-May|2011-May|2012-May|2013-May|'
                            r'2009-June|2010-June|2011-June|2012-June|2013-June|'
                            r'2009-July|2010-July|2011-July|2012-July|2013-July|'
                            r'2009-August|2010-August|2011-August|2012-August|2013-August|'
                            r'2009-September|2010-September|2011-September|2012-September|2013-September|'
                            r'2009-October|2010-October|2011-October|2012-October|2013-October|'
                            r'2009-November|2010-November|2011-November|2012-November|2013-November|'
                            r'2009-December|2010-December|2011-December|2012-December|2013-December)\b')

date_range_ii = re.compile(r'\bhttps://mailman\.nanog\.org/pipermail/nanog/('
                            r'2014-January|2015-January|2016-January|2017-January|2018-January|'
                            r'2014-February|2015-February|2016-February|2017-February|2018-February|'
                            r'2014-March|2015-March|2016-March|2017-March|2018-March|'
                            r'2014-April|2015-April|2016-April|2017-April|2018-April|'
                            r'2014-May|2015-May|2016-May|2017-May|2018-May|'
                            r'2014-June|2015-June|2016-June|2017-June|2018-June|'
                            r'2014-July|2015-July|2016-July|2017-July|2018-July|'
                            r'2014-August|2015-August|2016-August|2017-August|2018-August|'
                            r'2014-September|2015-September|2016-September|2017-September|2018-September|'
                            r'2014-October|2015-October|2016-October|2017-October|2018-October|'
                            r'2014-November|2015-November|2016-November|2017-November|2018-November|'
                            r'2014-December|2015-December|2016-December|2017-December|2018-December)\b')

date_range_iii = re.compile(r'\bhttps://mailman\.nanog\.org/pipermail/nanog/('
                            r'2019-January|2020-January|2021-January|2022-January|2023-January|'
                            r'2019-February|2020-February|2021-February|2022-February|2023-February|'
                            r'2019-March|2020-March|2021-March|2022-March|2023-March|'
                            r'2019-April|2020-April|2021-April|2022-April|2023-April|'
                            r'2019-May|2020-May|2021-May|2022-May|2023-May|'
                            r'2019-June|2020-June|2021-June|2022-June|2023-June|'
                            r'2019-July|2020-July|2021-July|2022-July|2023-July|'
                            r'2019-August|2020-August|2021-August|2022-August|2023-August|'
                            r'2019-September|2020-September|2021-September|2022-September|2023-September|'
                            r'2019-October|2020-October|2021-October|2022-October|2023-October|'
                            r'2019-November|2020-November|2021-November|2022-November|2023-November|'
                            r'2019-December|2020-December|2021-December|2022-December|2023-December)\b')

page = requests.get(main_url)
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find_all('tr')

threads = []
previous_dates = []
actual_dates = []
current_dates = []

links_matched_keywords_i = []
links_matched_keywords_ii = []
links_matched_keywords_iii = []

for row in table:
    thread = row.find('a')
    if thread is not None:
        current_year = main_url+thread['href']
        threads.append(current_year)

for link in threads:
    if re.match(date_range_i, link):
        previous_dates.append(link)
    if re.match(date_range_ii, link):
        actual_dates.append(link)
    if re.match(date_range_iii, link):
        current_dates.append(link)
  
for url in previous_dates:
    response = requests.get(url)
    content  = response.content
    soup     = BeautifulSoup(content, 'html.parser')

for url in actual_dates:
    response = requests.get(url)
    content  = response.content
    soup     = BeautifulSoup(content, 'html.parser')

for url in current_dates:
    response = requests.get(url)
    content  = response.content
    soup     = BeautifulSoup(content, 'html.parser')

for link in previous_dates:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    combined_threadlinks = soup.find_all('a', href=True)

    for tag in combined_threadlinks:
        if tag is not None:
            for keyword in keywords:
                if keyword in tag.text:
                    keyword_text = tag.text
                    keyword_url = link.replace("thread.html","")+tag['href']
                    links_matched_keywords_i.append([keyword_text, keyword_url]) # Why is these keywords in a list "[]"?

for link in actual_dates:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    combined_threadlinks = soup.find_all('a', href=True)

    for tag in combined_threadlinks:
        if tag is not None:
            for keyword in keywords:
                if keyword in tag.text:
                    keyword_text = tag.text
                    keyword_url = link.replace("thread.html","")+tag['href']
                    links_matched_keywords_ii.append([keyword_text, keyword_url])

for link in current_dates:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    combined_threadlinks = soup.find_all('a', href=True)

    for tag in combined_threadlinks:
        if tag is not None:
            for keyword in keywords:
                if keyword in tag.text:
                    keyword_text = tag.text
                    keyword_url = link.replace("thread.html","")+tag['href']
                    links_matched_keywords_iii.append([keyword_text, keyword_url])

df_range_i   = pd.DataFrame(links_matched_keywords_i, columns=['Subject', 'URL'])
df_range_ii  = pd.DataFrame(links_matched_keywords_ii, columns=['Subject', 'URL'])
df_range_iii = pd.DataFrame(links_matched_keywords_iii, columns=['Subject', 'URL'])

df_range_i.drop_duplicates(subset=['Subject'], inplace=True)
df_range_ii.drop_duplicates(subset=['Subject'], inplace=True)
df_range_iii.drop_duplicates(subset=['Subject'], inplace=True)

df_range_i.to_csv('potential-hijacks_2009-2013.csv', index=False)
df_range_ii.to_csv('potential-hijacks_2014-2018.csv', index=False)
df_range_iii.to_csv('potential-hijacks_2019-2023.csv', index=False)