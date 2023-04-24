
import pandas as pd
import requests
import re
from csv import writer
from bs4 import BeautifulSoup

with open("result.csv", "w", encoding="utf8", newline="") as f:
    thewriter = writer(f)
    header = ["Company", "Person"]
    thewriter.writerow(header)
    i=1
    pageno = 45
    while i <= pageno:

       # URL = "https://www.myrubbercouncil.com/marketplace/public/search_product.php?page="+str(i)+"&prokeyword=rubber&category=&subcategory=&rubber_type=&supkeyword=&state_id=&buss_id="
        URL = "https://www.myrubbercouncil.com/marketplace/public/search_supplier.php?page="+str(i)+"&prokeyword2=bhd"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        lists = soup.find_all("div", class_="box4a")

        for list in lists:
            company = list.find("h2").text.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ' ", "")
            person = list.find("div" , class_="detail").text.replace("\n", ",")
            info = [company, person]
            thewriter.writerow(info)
            print(info)
            
        i = i + 1


#DATA CLEANING IN CSV
data=pd.read_csv(r'c:\users\t520\documents\Github\result.csv', encoding = "ISO-8859-1")
data = data.replace(to_replace ='[\r\t]', value = '', regex = True)

data1 = data.Person.str.split(',', expand=True)
#data2 =pddata.Company
#data2 =data1.iloc[:,[0,1,5,16,17]]
data2 = pd.concat([data.Company, data1.iloc[:,[0,1,5,16,17]]], axis=1)
#print(data2.head(10).to_string())
#data4.drop('BBB', inplace=True, axis=1)
data2.columns = ['Company','Name', 'Email', 'Tel', 'Fax', 'Website']

data2.Company = data2.Company.str.replace('^\d+', '', regex=True)
data2.Name = data2.Name.str.replace(r"Contact Person: ", "", regex=True)
data2.Email = data2.Email.str.replace(r"Email: ", "", regex=True)
#Telephone = data2.Tel.str.replace(r"Tel: ", " ", regex=True)
data2.Fax = data2.Fax.str.replace(r"Fax: ", "", regex=True)
data2.Website = data2.Website.str.replace(r"Website: ", "", regex=True)

#data3 =  pd.concat([Name, Email, Telephone, Fax, Website], axis=1)
#print(data3)
print(data2.head(10).to_string())
#data4 =  pd.concat([data.Company, data3], axis=1)
#data4.drop('BBB', inplace=True, axis=1)
data2.to_csv(r'c:\users\t520\documents\Github\rubbercompany.csv', index=False)
