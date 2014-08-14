from lxml import etree
from lxml.html.clean import Cleaner
import sys

doc = open(sys.argv[1]).read()
cleaner = Cleaner(page_structure=False)
                  
doc=cleaner.clean_html(doc)
tree = etree.HTML(doc)

# gives the heading
# heading = tree.xpath('//*[@id="firstClickFreeAllowed"]/div[1]/div/div[1]/div/div/div/header/h2')
# print etree.tostring(heading[0],pretty_print=True)

# gives the defination
definations = tree.xpath('//*[@id="firstClickFreeAllowed"]/div[1]/div')
totalmeanings = len(definations)
i=1
print '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" class="no-js">
<body class=" ad_trick">
'''
for defi in definations:
    
    print etree.tostring(tree.xpath('//*[@id="firstClickFreeAllowed"]/div[1]/div['+str(i)+']/div[1]')[0],pretty_print=True)
    
    i=i+1
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
