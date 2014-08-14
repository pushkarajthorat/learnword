from lxml import etree
from lxml.html.clean import Cleaner
import sys

doc = open(sys.argv[1]).read()
# cleaner = Cleaner(page_structure=False)
#                    
# doc=cleaner.clean_html(doc)
tree = etree.HTML(doc)

# gives the heading
# heading = tree.xpath('//*[@id="firstClickFreeAllowed"]/div[1]/div/div[1]/div/div/div/header/h2')
# print etree.tostring(heading[0],pretty_print=True)

# gives the defination

defination1 = tree.xpath('//*[@id="rpane"]/div[3]/div/div/div/div[1]/div[2]/div')
defination2 = tree.xpath('//*[@id="rpane"]/div[4]/div[1]/div[2]')

print '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" class="no-js">
<body>
'''

print defination1,defination2
print etree.tostring(defination1,pretty_print=True)
print etree.tostring(defination2,pretty_print=True)
 
print '''
    </body>
</html>
'''
    #'/html/body/div/div/div/div/div[2]''
    #i=i+1

# defination = tree.xpath('//*[@id="firstClickFreeAllowed"]/div[1]/div[2]/div[1]/div/div/div/div[1]/div/section[1]')
# print etree.tostring(defination[0],pretty_print=True)
# 
# print "<h1>Derivatives</h1>"
# r = tree.xpath('//*[@id="firstClickFreeAllowed"]/div[1]/div/div[1]/div/div/div/section/dl/div')
# for element in r:
#     print etree.tostring(element,pretty_print=True)
