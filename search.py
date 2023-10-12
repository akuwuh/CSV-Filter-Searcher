import requests
import threading
from queue import Queue
import csv
from bs4 import BeautifulSoup

results = {}

def google_search(query, num_results=10):
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        search_results = soup.find_all("a")
        
        for result in search_results:
            link = result.get("href")
            if link.startswith("/url?q="):
                # Extract the actual URL from the Google search results link
                url = link.split("/url?q=")[1].split("&")[0]
                return url
    else:
        print("Failed to retrieve search results.")

def worker():
    while True:
        query = url_queue.get()
        global total
        if query is None:
            break
        result = google_search(query)
        global counter
        counter += 1
        print( str(counter) + "/" + str(total) + ": Finished Scraping " + query)
        results[query] = result
        url_queue.task_done()

def export(results):
    file_name = ""  # file name + path to export
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        columns = ['School Name', 'Url', 'Contact Info', 'Name', 'Role']
        csv_writer.writerow(columns)

        for name,url in results.items():
            csv_writer.writerow([name.strip(), url, ' ', ' '])

path = "" # path for search terms txt
with open(path, 'r') as file:
    search_queries = file.readlines()

num_threads = 4
url_queue = Queue()

urls = []
total = len(search_queries)
counter = 0
for query in search_queries:
    url_queue.put(query)

# Create and start worker threads
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
url_queue.join()

for _ in range(num_threads):
    url_queue.put(None)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("\nScraping Complete. Exporting..")

export(results)
print()
print("Export Complete")




