import re,glob
validEmail = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress
list_wishlists = glob.glob("Wishlists/*.csv") #gets list of wishlists
print(list_wishlists)
for item in list_wishlists:
    print(item)
    a = validEmail.search(item)
    print(a.group(0))
