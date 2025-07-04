import requests

# Publicly available file URLs
file_urls = [
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",  
    "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv",  
    "https://github.com/AyushPandey003/AyushPandey003/blob/main/README.md"  
]

for url in file_urls:
    print(f"Downloading from: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        filename = url.split("/")[-1]
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded successfully.\n")
    else:
        print(f"Failed to download file from {url}\n")
