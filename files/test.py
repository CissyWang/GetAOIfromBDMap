import re


name = "南京大学"
nameQ = "南京大学()"

url = "oreilly.com"
regex3 = re.compile(r"^((/|.)*(%s))" %url)
regex5 = re.compile(r"^((/|.)*"+ url +')')
reg = re.compile(r"^((%s)+(.(?!-).)*)"%name)
string3 = '/oreilly.com/baidu.com'

mo3 = regex3.search(string3)

mo5 = regex5.search(string3)
print(mo3.group())

print(mo5.group())
mo = reg.match(nameQ)
if mo!=None:
    print(True)
b = nameQ.endswith(")")|nameQ.endswith("学")
condition =(nameQ.endswith((")","学","区","院","校")))&(mo!=None)
print(condition)
