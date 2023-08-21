from xml.etree import ElementTree as ET
import re
import csv
tree = ET.parse(r"WikiPsampledump.txt")
root = tree.getroot()
pageRegex = "\[\[(([A-Za-z\s?]+)(\|[A-Za-z\s?]+)*)\]\]"

namespaces = {'x': "http://www.mediawiki.org/xml/export-0.10/"}
f = open("pageInfo.txt", "a")

counter = 1
for page in root.findall('x:page', namespaces):
    internalLinks = []
    pageInfo = []
    if counter == 3:
        break
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
    f.write(pageId.text + ", " + pageTitle.text + ", " +
            pageNs.text + ", " + contributor.text + ", ")
    for intLink in internalLinks:
        f.write(intLink + ", ")
    f.write("\n")
    counter += 1


#     CustomerId = customer.find('x:CustomerId', namespaces).text

#             for customer in root.findall('x:Customer', namespaces):

#             CustomerId = customer.find('x:CustomerId', namespaces).text

#             Email = customer.find('x:Email', namespaces).text

#             Name = customer.find('x:Name', namespaces).text

#             Age = customer.find('x:Age', namespaces).text

#          LineData = OrderDetail.findall('x:Lines', namespaces)
