import yaml

with open("creds.yaml") as file:
    documents = yaml.full_load(file)
print(documents)
