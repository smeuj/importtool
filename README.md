# importtool
This project consists of several scripts to aid in selecting smeuj from WhatsApp
chat logs and converting them to a consistent datastructure.
`src/parse_whatsapp.py` parses a WhatsApp chat log and converts it to json.
`src/smeuj.py` allows one to view the chat messages and save smeuj to json.
`src/unique_authors.py` prints all unique message authors from a chat json file.
`src/map_names.py` allows one to replace all author names in chat json with
other names.
`src/join_chats.py` combines two partially overlapping chat json files.

All commands presented in this README file should be run from this project's
root directory (the same directory where this README file is located) unless
otherwise specified.

## Usage
### parse_whatsapp
This script is run as follows:

    python src/parse_whatsapp.py <input_path> <output_path>

Here `<input_path>` specifies a text file containing a WhatsApp chat log.
The chat log is assumed to be formatted as exported from WhatsApp.
`<output_path>` specifies the path where the output json will be saved.

### smeuj
This script is run as follows:

    python src/smeuj.py <chat_path> <smeuj_path>

Here `<chat_path>` specifies a json file containing WhatsApp chat entries.
The json generated by the parsing script is a valid input here.
`<smeuj_path>` specifies a json file containing a collection of smeuj.
If the file doesn't exist yet, a new one will be created with an empty
collection.

This script presents an interface consisting of several main parts.
At the top, a table containing all the smeuj is presented.
Under that is the WhatsApp chat log.
Under the chat log are entry fields which one can use to enter the details of
a smeu.
Click the "Add" button to add the smeu to the smeuj list.
To delete smeuj, select them in the smeuj list and click the "Delete" button.
Click a message in the chat log to automatically fill the relevant entry fields
with that message's data.
You can also use the "Next" and "Previous" buttons to move forwards or backwards
through the messages.

Whenever the list of smeuj is changed, it is automatically updated in the json
file.
There is no need to manually save anything before closing the application.

### unique_authors
This script is run as follows:

    python src/unique_authors.py <chat_path>

Here `<chat_path>` specifies a json file containing WhatsApp chat entries.
The script prints a list of all unique message author names to the console.

### map_names
This script is run as follows:

    python src/map_names.py <chat_path> <name_path> [output_path]

Here `<chat_path>` specifies a json file containing WhatsApp chat entries.
`<name_path>` specifies a json file containing a single object with keys and
values in the format:

    "source name": "dest name"

Every message author name in the chat file that matches the source name will be
replaced by the dest name.
If `[output_path]` is given, the output is written to that path; otherwise, the
output is written back to `<chat_path>`.

### join_chats
This script is run as follows:

    python src/join_chats.py <output_path> <chat_paths...>

Here `<output_path>` is the path to which the combined chat file will be saved.
`<chat_paths...>` is a list of partially overlapping chat json files
_in chronological order_.
Every path is given as a seperate argument to the script and thus, each path
needs to be seperated by a space in this command.
