# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses
from bs4 import BeautifulSoup

from .cache import cache
from .http import get_html_with_cache
from .paths import path_ts_data, path_ts_setting


CACHE_EXPIRE = 24 * 3600  # 24 hours


base_url = "https://docs.aws.amazon.com"
homepage_url = f"{base_url}/cdk/api/v2/docs/aws-construct-library.html"
cdk_lib_href_prefix = "/cdk/api/v2/docs/aws-cdk-lib.aws_"


@dataclasses.dataclass
class Link:
    srv_name: str
    res_type: str
    res_name: str
    url: str


# @cache.memoize(expire=CACHE_EXPIRE)
def get_links():
    html = get_html_with_cache(homepage_url)
    soup = BeautifulSoup(html, "html.parser")
    div_doc_nav = soup.find("div", id="docsNav")

    sub_group_type_set = set()

    links = list()
    for div_suv_nav_group in div_doc_nav.find_all("div", class_="navGroup subNavGroup"):
        h4 = div_suv_nav_group.find("h4")
        if h4 is None:
            # print(div_suv_nav_group.text)
            continue
        sub_group_type = h4.text
        sub_group_type_set.add(sub_group_type)
        res_type = sub_group_type
        for a in div_suv_nav_group.find_all("a", class_="navItem"):
            href = a.attrs["href"]
            if href.startswith(cdk_lib_href_prefix):
                href_new = href.replace(cdk_lib_href_prefix, "")
                srv_name = href_new.split(".")[0]
                res_name = a.text
                url = f"{base_url}{href}"
                link = Link(
                    srv_name=srv_name,
                    res_type=res_type,
                    res_name=res_name,
                    url=url,
                )
                links.append(link)

    sub_group_type_list = list(sub_group_type_set)
    sub_group_type_list.sort()
    return links


def build_data():
    docs = list()
    links = get_links()
    for link in links:
        doc = dict(
            srv_name=link.srv_name,
            res_type=link.res_type,
            res_name=link.res_name,
            url=link.url,
        )
        docs.append(doc)

    setting = {
        "fields": [
            {
                "name": "srv_name",
                "type_is_store": True,
                "type_is_ngram": True,
                "ngram_maxsize": 10,
                "ngram_minsize": 2,
                "weight": 5.0,
            },
            {
                "name": "res_type",
                "type_is_store": True,
                "type_is_ngram": True,
                "ngram_maxsize": 10,
                "ngram_minsize": 2,
                "weight": 3.0,
            },
            {
                "name": "res_name",
                "type_is_store": True,
                "type_is_ngram": True,
                "ngram_maxsize": 10,
                "ngram_minsize": 2,
                "weight": 1.0,
            },
            {
                "name": "url",
                "type_is_store": True,
            },
        ],
        "title_field": "{srv_name} - {res_type} | {res_name}",
        "subtitle_field": "{url}",
        "arg_field": "{url}",
        # "autocomplete_field": "{service} - {res_type} | {res_name}",
    }

    path_ts_data.write_text(json.dumps(docs, indent=4))
    path_ts_setting.write_text(json.dumps(setting, indent=4))
