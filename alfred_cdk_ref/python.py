# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses
from bs4 import BeautifulSoup

from .cache import cache
from .http import get_html_with_cache
from .paths import path_python_data, path_python_setting

CACHE_EXPIRE = 24 * 3600  # 24 hours

base_url = "https://docs.aws.amazon.com/cdk/api/v2/python"
homepage_url = f"{base_url}/index.html"


@dataclasses.dataclass
class Service:
    name: str
    url: str


@cache.memoize(expire=CACHE_EXPIRE)
def get_services() -> T.List[Service]:
    html = get_html_with_cache(homepage_url)
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("section", id="aws-cdk-python-reference")
    services = list()
    for a in section.find_all("a"):
        if (a.text != "API Reference") and (
            a.attrs.get("title", "") != "Permalink to this heading"
        ):
            name = a.text
            url = "{}/{}".format(base_url, a.attrs["href"])
            service = Service(name, url)
            services.append(service)
    return services


@dataclasses.dataclass
class Link:
    service_name: str
    object_name: str
    object_url: str

    @property
    def is_cfn(self) -> bool:
        return self.object_name.startswith("Cfn")

    @property
    def service_name_facet(self) -> str:
        return self.service_name.replace("aws_cdk.aws_", "").replace("aws_cdk.", "")

    @property
    def object_name_facet(self) -> str:
        return self.object_name


@cache.memoize(expire=CACHE_EXPIRE)
def get_links(service_name: str, service_url: str) -> T.List[Link]:
    tag_id = service_name.replace("_", "-").replace(".", "-")
    html = get_html_with_cache(service_url)
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("section", id=tag_id)
    links = list()
    for a in section.find_all("a"):
        if a.attrs.get("title", "") != "Permalink to this heading":
            object_name = a.text
            object_url = "{}/{}".format(base_url, a.attrs["href"])
            link = Link(service_name, object_name, object_url)
            links.append(link)
    return links


def build_data():
    docs = list()
    for service in get_services():
        links = get_links(service.name, service.url)
        for link in links:
            doc = dict(
                service=link.service_name_facet,
                object=link.object_name_facet,
                url=link.object_url,
            )
            docs.append(doc)

    setting = {
        "fields": [
            {
                "name": "service",
                "type_is_store": True,
                "type_is_ngram": True,
                "ngram_maxsize": 10,
                "ngram_minsize": 2,
                "weight": 5.0,
            },
            {
                "name": "object",
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
        "title_field": "{service} - {object}",
        "subtitle_field": "{url}",
        "arg_field": "{url}",
        "autocomplete_field": "{service} {object}",
    }

    path_python_data.write_text(json.dumps(docs, indent=4))
    path_python_setting.write_text(json.dumps(setting, indent=4))
