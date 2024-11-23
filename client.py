import asyncio
import websockets
import signal

def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')
    # Perform any cleanup or exit logic here
    exit(0)

# Set the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)


options_string = "Choose \n1. Get inventory data. \n2. Write data. \n3.Read data"

async def client():

    try:

        async with websockets.connect("ws://localhost:8765") as websocket:
            while True:

                message = input("")
                if message == "4":
                    await websocket.close()
                
                if message == "1":
                    await websocket.send(message)
                    message_from_server = await websocket.recv()
                    print(message_from_server)

                if message == "2":
                    key_to_write = input("Enter the key name you want to write:")
                    await websocket.send(message+"-"+key_to_write)
                    message_from_server = await websocket.recv()
                    print(message_from_server)
                    vall = input("")
                    await websocket.send(message+"-"+key_to_write+"-"+vall)
                    message_from_server = await websocket.recv()
                    print(message_from_server)

                if message == "3":
                    key_to_read = input("Enter the key name you want to read:")

                    await websocket.send(message+"-"+key_to_read)
                    message_from_server = await websocket.recv()
                    print(message_from_server)

                    message_from_server = await websocket.recv()
                    print(message_from_server)
    except:
        print("Error, pl check if you provided correct keys to read or write")




            #print(f"Received message: {message}")

if __name__ == "__main__":
    print("Welcome to the server. Choose \n1. Get inventory data. \n2. Write data. \n3.Read data \n4. Exit/disconnect client")
    
    asyncio.run(client())
