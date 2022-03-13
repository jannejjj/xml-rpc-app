from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET

server = SimpleXMLRPCServer(('localhost', 8000))


def savedata(topic, title, text, timestamp):
    print("The save function was called")
    # read initial data from db.xml and get the root
    tree = ET.parse('db.xml')
    root = tree.getroot()

    try:
        # Check if the topic exists already
        given_topic = root.find("topic[@name='" + topic + "']")
        if given_topic is not None:
            new_note = ET.SubElement(given_topic, "note", name=title)  # Add new note as subelement to given topic
            ET.SubElement(new_note, "text").text = text
            ET.SubElement(new_note, "timestamp").text = timestamp
        else:
            new_topic = ET.SubElement(root, "topic", name=topic)  # Add given topic as a subelement to root
            new_note = ET.SubElement(new_topic, "note", name=title)
            ET.SubElement(new_note, "text").text = text
            ET.SubElement(new_note, "timestamp").text = timestamp
    except:
        print("There was an error saving the data!")
        return False

    tree.write('db.xml')
    return 'Data saved to database!\n'


def readdata(topic):
    print("The read function was called")
    # Read data from db.xml and get the root
    tree = ET.parse('db.xml')
    root = tree.getroot()
    data = []

    try:
        # Find the topic element given and return it, else return an error message
        element = root.find("topic[@name='" + topic + "']")
        print(ET.tostring(element))
        if element is not None:
            notes = element.findall("note")
            # Get data from each note, append to list and finally return the list
            for note in notes:
                title = note.get('name')
                text = note.find("text").text
                timestamp = note.find("timestamp").text
                data.append(f'Title: {title}\n'
                            f'Note: {text}\n'
                            f'Timestamp {timestamp}')
            return data
        else:
            return False
    except:
        print('There was an error reading the data!')
        return False


# Register the functions and start server
server.register_function(savedata, 'save')
server.register_function(readdata, 'read')
print("Server listening at port 8000...")
server.serve_forever()
