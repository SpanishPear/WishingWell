import glob
import os
import csv
import re
emailAddr = 'shrey.somaiya@gmail.com' #stimulate the emailAddr in the main program
def ListWishlists():
    '''Takes directory of wishlists, and returns the file path of all the wishlists'''
    list_wishlists = glob.glob("Wishlists/*.csv")
    return list_wishlists #returns list of wishlists
def OpenWishlists(list_paths):
    '''Locates, opens, and outputs the contents of every wishlist'''
    pattern = re.compile(r'\/.*-')
    for i in range(len(list_paths)):
        wishlist_name = pattern.findall(list_paths[i])[0][1:-1]
        print("\n"+ wishlist_name+":")
        with open(list_paths[i]) as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(row['items'])
def OpenWishlistFromPath(wishlist_path):
    '''Locates, opens, and outputs the contents a wishlist given its path'''
    pattern = re.compile(r'\/.*-')
    wishlist_name = pattern.findall(wishlist_path)[0][1:-1]
    print(wishlist_name+":")
    with open(wishlist_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['items'])
def OpenWishlistFromName(wishlist_name):
    '''Locates, opens and outputs the contents of a wishlist given its name'''
    print(wishlist_name+":")
    wishlist_path = "Wishlists/"+wishlist_name + "-" +emailAddr+'.csv'
    with open(wishlist_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['items'])    
#OpenWishlists(ListWishlists())
#OpenWishlistFromPath('Wishlists/18th_birthday-shrey.somaiya@gmail.com.csv')
#OpenWishlistFromName("18th_birthday")
