from flask import Flask, request
from threading import Thread
import requests
import random
from time import sleep
from products import products

# Create a Flask object called app
app = Flask(__name__)

# Array to store the threads
threads = []

# App route
@app.route('/producer', methods = ['GET', 'POST'])

def create_client(name):
    try:
        client_id = name
        product = random.choice(products)
        order_id = int(random.random() * random.random() / random.random() * 1000)
        payload = dict({'order_id': order_id, 'client_id': client_id, 'product_id': product['id']})
        print(f"Client nr.{name} has ordered a {product['name']} which costs {product['price']}$. Order nr.{order_id} is sent to the order service.")
        requests.post('http://localhost:4040/producer_aggregator', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass

def run_producer():
    producer_thread = Thread(target=lambda: app.run(host = '0.0.0.0', port = 4000, debug = False, use_reloader = False), daemon = True)
    producer_thread.start()
    sleep(2)
    thread_name = 1
    # Create thread Client
    for _ in range(7):
        thread = Thread(target = create_client, args = (thread_name,), name = str(thread_name))
        threads.append(thread)
        thread_name += 1
    for thread in threads:
        thread.start()
        sleep(2)
    for thread in threads:
        thread.join()
    while True:
        pass

if __name__ == '__main__':
    run_producer()