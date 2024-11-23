# DistributedLocker
## Distributed locker for key value pairs

## Steps to run

### Pre-requisites
1. Python is installed in the system
2. asyncio and websockets are installed (using pip or any python module downloader)

### Steps to run
1. Start the server using `python3 server.py`
2. Start the client using `pytohn3 client.py`. You can start as many clients as required to simulate a distributed environment. Follow instructions in the client to choose options to view all the exisitng keys, read, write or terminate the client. 

## Functionalities

1. Multiple clients can write different value for the existing key value pairs defined in the server.
2. I have added a 30 sec delay for read and write operations to simlulate long running read and write.
3. If one client is writing, others cannot write to the same key.
4. If a key is being read by a client then writing is not allowed too.

## Assumptions and limitaitons

1. A single client cannot do multiple reads/write while an existing operation is in progress. Couldn't do a good job with intercepting main thread running asyncio. But diffrent clients can do read/writes simultaneously.

2. There is no way to see the overall data. Only way is by doing reads on particular keys.

3. Simulating client disconnect is done using ctrl+c or typing 4 in the client code. Havent covered other different ways of disconnecting.

4. Error handling isn't very robust. 

Note: The command `kill -9 $(lsof -ti:8765)` will be handy if runing server multiple times to unbiind the port.