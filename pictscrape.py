import requests
import re
import sys
import json
from threading import Thread
import time
from colors import *

mylist=['http://faculty.pictinc.org/AS/AS-Faculty.aspx',
        'http://faculty.pictinc.org/EnTC/EnTC-Faculty.aspx',
        'http://faculty.pictinc.org/computer/CE-Faculty.aspx',
        'http://faculty.pictinc.org/IT/IT-Faculty.aspx']

baseurl = "http://faculty.pictinc.org/Faculty-Profile.aspx?profileID="

valid_ids = []

if len(sys.argv) != 2:
    print(brightgreen+"Usage: {} <No of threads>\n".format(sys.argv[0]),end)
    print(green,"Example: python {} 5".format(sys.argv[0]),end)
    sys.exit()

print(cyan,"[!] Getting ID's",end)
for i in mylist:
    r = requests.get(i)
    valid_ids+=re.findall(r'profileID=(\d{1,3})',r.text)

print(cyan,"[!] Total {} ID's found".format(len(valid_ids)),end)

thelist = valid_ids
data = []
def work():
    while thelist != []:
        i = thelist.pop()
        url = baseurl+i
        r = requests.get(url)
        sys.stdout.write(green+" [+] Scraping id {}".format(i)+"\n")
        Name = re.findall(r'<b style="color:#2E73B5">(.*)</b>',r.text)
        Profileimage = re.findall(r'UploadImages/(.*).(jpg|JPG|jpeg|png|JPeG|PNG|JPEG|Jpeg|Jpg|Png|Gif)',r.text)
        fullname = re.findall(r'Name:</b>(.*)\s+</td>',r.text)
        department = re.findall(r'Department:</b>(.*)\s+</td>',r.text)
        designation = re.findall(r'Designation:</b>(.*)\s+</td>',r.text)
        emailid = re.findall(r'Email-ID:</b>(.*)\s+</td>',r.text)
        phone = re.findall(r'Phone No:</b>(.*)\s+</td>',r.text)

        Profileimage = Profileimage[0][0]+"."+Profileimage[0][1]
        Name = Name[2]
        fullname = fullname[0].strip('\r')
        department = department[0].strip('\r')
        designation = designation[0].strip('\r')
        emailid = emailid[0].strip('\r')
        phone = phone[0].strip('\r')

        d = {}
        d["Name"] = Name.capitalize()
        d["ProfileImage"] = Profileimage
        d["FullName"] = fullname
        d["Department"] = department
        d["Designation"] = designation
        d["Email"] = emailid
        d["Phone"] = phone
        data.append(d)
        time.sleep(0.5)
        
sys.stdout.write(end)

tlist = []
print(yellow,"[*] Working with {} threads".format(sys.argv[1]),end)
tcount = int(sys.argv[1])
for i in range(tcount):
    t = Thread(target=work)
    t.start()
    tlist.append(t)

for t in tlist:
    t.join()

with open("data.json", "w") as f:
    f.write(str(json.dumps(data)))
    print(yellow,"[*] Data Written to data.json ",end)
