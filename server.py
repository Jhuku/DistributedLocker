import asyncio
import websockets
import time

connected_clients = set()

options_string = "\nChoose \n1. Get inventory data. \n2. Write data. \n3.Read data \n4. Exit/disconnect client."

data = {
    "Apple": 1234,
    "Ball": 3419,
    "Cat": 8972,
    "Dog": 77777
}

read_write_stats = {}

def create_read_write_stats(rrs, data):
     # create a dict 
     read_write_stats = {}
     for item in data:
        #  print(":Item = "+str(item))
         rrs[item] = {"Writer":0, "Readers":[]}
    
    #  return read_write_stats

async def writingtask():
    print("Task writing started")
    await asyncio.sleep(30)
    print("Task writing finished")

async def readingtask():
    print("Task reading started")
    await asyncio.sleep(30)
    print("Task reading finished")

async def handle_client(websocket):
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Received message from {websocket.remote_address}: {message}")
            if message == "1":
                print("Client wants to get inventory items")
                data_keys = data.keys()
                await websocket.send("Here are the items currently in the inventory: \n" +str(list(data_keys)) + options_string)
            elif message.startswith("2"):
                messages = message.split("-")
                if len(messages) == 1:
                    print("WRITE option selected")
                elif len(messages) == 2:
                    key_to_write = message.split("-")[1]
                    print("The key for write is selected = "+key_to_write)

                    # can only write when noone is wrting or reading the key
                    if read_write_stats[key_to_write]["Writer"] == 0 and not read_write_stats[key_to_write]["Readers"]:
                        print(key_to_write+" can be written by this client")
                        await websocket.send("You can write now, enter the new value: ")
                    else:
                        print(key_to_write+" cannot be written as it is being written/read by others")
                        await websocket.send("you cannot write as it is being written/read by others. Please wait till write/read is finishied : "+options_string)

                elif len(messages) == 3:
                    print("The value is sent...writing.....")
                    # set write lock
                    read_write_stats[key_to_write]["Writer"]=str(websocket.remote_address[1])
                    await websocket.send("Value is being written.... "+options_string)
                    # writing is happenning as a long process
                    await asyncio.gather(writingtask())
                    # after writing is done release the write lock
                    read_write_stats[key_to_write]["Writer"] = 0
                    print("Data stat = "+str(read_write_stats))
                    data[messages[1]] = messages[2]
                    print("Now data = ", data)

            elif message.startswith("3"):
                print("Client wants to READ")
                messages = message.split("-")

                if len(messages) == 1:
                    print("READ option selected")
                
                if len(messages) == 2:
                    key_to_read = message.split("-")[1]
                    print("Reading key..... = "+key_to_read)
                    

                    # set reading stat
                    read_write_stats[key_to_read]["Readers"].append(str(websocket.remote_address[1]))      
                    print("Data stat original = "+str(read_write_stats))
                    await websocket.send("Value is being read.... ")
                    # reading is happenning as a long running process
                    await asyncio.gather(readingtask())
                    # after reading is done release the read lock i.e remove the client from Readers
                    readers_list = read_write_stats[key_to_read]["Readers"]
                    readers_list.remove(str(websocket.remote_address[1]))
                    read_write_stats[key_to_read]["Readers"] = readers_list
                    await websocket.send("The value is =  "+str(data[key_to_read])+options_string)
                    print("Data stat = "+str(read_write_stats))
            client_id = websocket.remote_address[1]
    except:
        print("Error occured, please check if you provided the correct key values")
    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")

        # free the write and readers lock for this client
        disconnected_client_id = websocket.remote_address[1]
        # traverse all keys in read_write_stats and check where the client is present
        print("Final stats is = "+str(read_write_stats))

        for key in read_write_stats:

            if str(read_write_stats[key]["Writer"]) == str(disconnected_client_id):
                read_write_stats[key]["Writer"] = 0
            
            if str(key) in read_write_stats[key]["Readers"]:
                readers = read_write_stats[key]["Readers"]
                readers.remove(str(key))
                read_write_stats[key]["Readers"] = readers
        
        print("Final stats after removal is = "+str(read_write_stats))



async def main():
    global read_write_stats
    create_read_write_stats(read_write_stats, data)
    # print(read_write_stats)
    async with websockets.serve(handle_client, "localhost", 8765, ping_interval=20, ping_timeout=900):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())