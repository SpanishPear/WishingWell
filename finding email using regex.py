import re
pattern = re.compile(r'[a-zA-Z]+\.[a-zA-Z]*@[a-zA-Z]+\.[a-zA-Z]*')
m = pattern.search("wishlists/shrey.somaiya@gmail.com-Valentines.csv")
print(m.group(0))
