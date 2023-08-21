from xml.etree import ElementTree as ET
import re
import csv

from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

tree = ET.parse(r"enwiki-latest-pages-articles.xml")
root = tree.getroot()
pageRegex = "\[\[(([A-Za-z\s?]+)(\|[A-Za-z\s?]+)*)\]\]"

uri = "neo4j+s://cd3e0bb5.databases.neo4j.io"
user = "neo4j"
password = "yYLYWppXajZFiT_QEEJfyrWo18cTRgOiRBztpBfDHHI"

driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session()


internalLinks = []
namespaces = {'x': "http://www.mediawiki.org/xml/export-0.10/"}
counter = 1
for page in root.findall('x:page', namespaces):
    pageTitle = page.find('x:title', namespaces)
    print("Page " + str(counter) + " Title: " + pageTitle.text)
    pageId = page.find('x:id', namespaces)
    print("Page " + str(counter) + " Id: " + pageId.text)
    pageNs = page.find('x:ns', namespaces)
    print("Page " + str(counter) + " ns: " + pageNs.text)
    for revision in page.findall('x:revision', namespaces):
        contributors = revision.findall('x:contributor', namespaces)
        for Contributor in contributors:
            contributor = Contributor.find('x:username', namespaces)
            print("Contributor: " + contributor.text + "\n")
        Text = revision.find('x:text', namespaces)
        object = re.finditer(pageRegex, Text.text)

    for match in object:
        if match.group(2) not in internalLinks:
            internalLinks.append(match.group(2))
            print(match.group(2))
    # Spot for connection and insertion
    print(type(pageTitle.text))
    print("yo" + "', '".join(internalLinks))
    query = "create (p:Page{Title:'"+pageTitle.text.upper() + \
        "', PageID:'"+pageId.text+"'})"
    querySetLinks = "match (p {Title: '"+pageTitle.text.upper(
    ) + "'}) set p.InternalLinks = ['" + ("', '".join(internalLinks).upper()) + "']"
    print(querySetLinks)
    result = session.run(query)
    result2 = session.run(querySetLinks)

    counter += 1

# create function that set relation ships


# Close session
session.close()
driver.close()
