import os
import sys
import time

pid = int(input("Enter PID of victim process: "))
new_secret = b"HackedByChatGPT!!"  # Must be same length or shorter

# Get the memory maps of the process
with open(f"/proc/{pid}/maps", 'r') as maps:
    for line in maps:
        if '[heap]' in line:
            addr_range = line.split(' ')[0]
            start, end = [int(x, 16) for x in addr_range.split('-')]
            break
    else:
        print("❌ No heap found.")
        exit()

# Open memory for read/write
with open(f"/proc/{pid}/mem", 'r+b', buffering=0) as mem:
    mem.seek(start)

    chunk = mem.read(end - start)
    location = chunk.find(b"ThisIsTheSecret123")

    if location == -1:
        print("❌ Could not find secret in memory.")
    else:
        print(f"✅ Found secret at offset {hex(start + location)}")
        mem.seek(start + location)
        mem.write(new_secret)
        print("✅ Memory injection complete.")
