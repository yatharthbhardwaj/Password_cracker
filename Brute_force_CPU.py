import itertools
import time
import os
import multiprocessing
import string

def crack_password(password, chars=string.ascii_letters + string.digits + "@$!"):
    start_time = time.time()
    combinations_tried = 0
    max_length = 15 # Maximum password length to attempt
    for length in range(1, max_length + 1):
        for attempt in itertools.product(chars, repeat=length):
            combinations_tried += 1
            attempt = ''.join(attempt)
            if attempt == password:
                end_time = time.time()
                return end_time - start_time, combinations_tried

def main():
    password = input("Enter the password to crack: ")
    
    # Split the character set into chunks to be processed by multiple cores
    chars = string.ascii_letters + string.digits + "@$!"
    chunk_size = len(chars) // 10
    chunks = [chars[i:i + chunk_size] for i in range(0, len(chars), chunk_size)]
    
    pool = multiprocessing.Pool(processes=8)
    results = [pool.apply_async(crack_password, (password, chunk)) for chunk in chunks]
    
    cracked_time = None
    total_combinations_tried = 0
    for result in results:
        time_taken, combinations_tried = result.get()
        total_combinations_tried += combinations_tried
        if time_taken is not None:
            cracked_time = time_taken
    
    if cracked_time is not None:
        print(f"Password cracked in {cracked_time:.2f} seconds.")
    else:
        print("Failed to crack the password.")
    
    print(f"Total combinations tried: {total_combinations_tried}")

if __name__ == "__main__":
    main()
