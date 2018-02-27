import csv, uuid, hashlib
def signUp(fullname, password, email):
    with open("users/salt.csv") as f:
        for line in csv.reader(f):
            salt = line[1]
            hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    with open("users/users.csv",'r+') as f:
        writer = csv.writer(f)
        for line in csv.reader(f):
            if line[0] == fullname:
                return False
            else:
                writer.writerow([fullname, hashed_password, email]) #stores hashed passsword
                return True
            
def login_validation(email, password):
    with open("users/salt.csv") as f:
        for line in csv.reader(f):
            salt = line[1]
            hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    with open("users/users.csv", 'r') as f:
        for line in csv.DictReader(f):
            hashedinput = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
            if line["password"] == hashedinput:
                return True
            else:
                return False
        
signUp('Shrey Somaiya','mdcNU#r@#I17', '106299@avondaleschool.nsw.edu.au')
login_validation('106299@avondaleschool.nsw.edu.au', 'mdcNU#r@#I17')
