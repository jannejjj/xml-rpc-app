from xmlrpc.client import ServerProxy
from datetime import datetime

proxy = ServerProxy('http://localhost:8000')

def select():
    print(
        "XMLRPC Client\n"
        "Options:\n"
        "1) - Input data\n"
        "2) - Read data by topic\n"
        "0) - Exit"
    )

    selection = input("Input: ")
    return int(selection)

def main():
    while True:
        selection = select()

        if selection == 1:
            topic = input("Topic of your note: ")
            title = input("Title of your note: ")
            text = input("Your note: ")
            now = datetime.now()
            timestamp = now.strftime("%d/%m/%Y - %H:%M:%S")

            msg = proxy.save(topic, title, text, timestamp)
            print(msg)
        elif selection == 2:
            topic = input("Topic to get data from: ")
            data = proxy.read(topic)

            if data is False:
                print('There was an error reading the data or no data was found.\n')
            else:
                print("\n")
                for note in data:
                    print(note)
                    print("\n")
        elif selection == 0:
            print("Thank you for using the program.")
            exit(0)
        else:
            print("Something went wrong, exiting..")
            exit(0)

main()