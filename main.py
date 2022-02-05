from fastapi import FastAPI
import requests
import json
import pandas as pd
from secrets import api_key


# Function to create address in string form
def create_address(dt: dict):
    street = str(dt.get("street"))
    suite = str(dt.get("suite"))
    city = str(dt.get("city"))
    zipcode = str(dt.get("zipcode"))

    address = f"{street}, {suite}, {city}, {zipcode}"
    return address


# Function to convert IDR to USD
def create_usd(n: float):
    return n * float(convertFactor)


# Gets JSON data from API
response = requests.get("http://jsonplaceholder.typicode.com/users").text
res = json.loads(response)

# Gets Salary data from JSON file
f = open("salary_data.json")
array = json.load(f)
salary = array.get("array")
f.close()

# Gets conversion factor
convertFactorAPI = requests.get(
    f"https://free.currconv.com/api/v7/convert?q=IDR_USD&compact=ultra&apiKey={api_key}").text
convertFactorJSON = json.loads(convertFactorAPI)
convertFactor = convertFactorJSON.get("IDR_USD")

# Converts json data into pandas dataframe to make things look cleaner
pd.set_option('display.max_columns', None)
df = pd.json_normalize(res, max_level=0)
df2 = pd.json_normalize(salary)

df3 = df.merge(df2)
df3 = df3[['id', 'name', 'username', 'email', 'address', 'phone', 'salaryInIDR']]
df_address = df3['address'].apply(create_address)
df_USD = df3['salaryInIDR'].apply(create_usd)
df3['address'] = df_address
df3['Salary in USD'] = df_USD
df3 = df3.rename(columns={"id": "ID", "name": "Name", "username": "Username", "email": "Email", "address": "Address",
                          "phone": "Phone", "salaryInIDR": "Salary in IDR"})

result = df3.to_json(orient="records", indent=4)
result_json = json.loads(result)


# Setting up the API endpoints
app = FastAPI()


@app.get("/")
async def root():
    return result_json


@app.get("/get-by-id/{person_id}")
async def get_person(person_id: int):
    for x in result_json:
        if x.get("ID") == person_id:
            return x
    return {"Data": "Not Found"}


@app.get("/get-by-name/{name}")
async def get_person(name: str):
    for x in result_json:
        if name in x.get("Name"):
            return x
    return {"Data": "Not Found"}


@app.get("/get-by-username/{username}")
async def get_person(username: str):
    for x in result_json:
        if x.get("Username") == username:
            return x
    return {"Data": "Not Found"}
