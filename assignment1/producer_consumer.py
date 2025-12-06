import queue
import threading
import time


# Example source and destination containers
source_data = [1,2,3,4,5]
destination_data = []

# Shared blocking queue
shared_queue = queue.Queue(maxsize=2)

# Marker to tell the consumer to stop
SENTINEL = object()

# Thread-safe prints
print_lock = threading.Lock()
def tprint(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

# Producer thread: reads from source and puts items into the shared queue.
def producer(source, q):
    tprint('[Producer] Starting')
    for item in source:
        tprint(f'[Producer] producing: {item}')
        q.put(item)
        time.sleep(0.1)
    tprint("[Producer] sending sentinel, done producing")
    q.put(SENTINEL)
    tprint('[Producer] Ending.')

# Consumer thread: takes items from the shared queue and writes to destination.
def consumer(destination, q):
    tprint('[Consumer] Starting')
    while True:
        item = q.get()
        if item is SENTINEL:
            tprint('[Consumer] received sentinel, done consuming')
            break
        tprint(f'[Consumer] consuming: {item}')
        destination.append(item)
        time.sleep(0.2)
    tprint('[Consumer] Ending.')

def main():
    # Set up and run producer and consumer in parallel threads
    producer_thread = threading.Thread(target=producer, args=(source_data, shared_queue))
    consumer_thread = threading.Thread(target=consumer, args=(destination_data, shared_queue))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    tprint("[Main] All done. Destination data:", destination_data)


if __name__ == "__main__":
    main()