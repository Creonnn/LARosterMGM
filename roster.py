from pymongo import MongoClient
import urllib, os, la_data, pymongo
from quickchart import QuickChart
from dotenv import load_dotenv

# Initiates MongoDB
load_dotenv()
password = urllib.parse.quote(os.getenv('PASSWORD'))
uri = f'mongodb+srv://Creonnn:{password}@cluster0.3ataaai.mongodb.net/'
cluster = MongoClient(uri)
db = cluster['discord']
roster_db = db['roster']

convert_keys = {
    'name': 'char_name',
    'class': 'class_name',
    'ilvl': 'ilvl',
    'engraving': 'class_eng'
}

def add(message: str, svr_id: str, disc_id: str) -> bool:
    '''
    Adds a character to user's roster

    -PARAMS-
    message: the message string. Syntax must be $add <char_name>, <class_name>, <ilvl>, <class_eng>
    svr_id: server id. A string of numbers
    disc_id: Discord id. a string of numbers
    return: True if successfully added. False otherwise
    '''
    data = [message.split(',')[i].strip().title() for i in range(len(message.split(',')))]
    char_name, class_name, class_eng, ilvl = data[0], data[1], data[2], float(data[3])

    query = roster_db.find({'svr_id': f"{svr_id}", 'char_name': char_name})
    # Check if char_name already exists for the user in that server
    if query_length(query) == 1:
        return False

    data = {'disc_id': disc_id, 'svr_id': svr_id, 'char_name': char_name, 'class_name': class_name, 'ilvl': ilvl, 'class_eng': class_eng}
    roster_db.insert_one(data)
    return True

'''
def add_using_image(char_name, class_name, ilvl, svr_id: str, disc_id: str):
    class_eng = "N/A"
    query = roster_db.find({'svr_id': f"{svr_id}", 'char_name': char_name})
    # Check if char_name already exists for the user in that server
    if query_length(query) == 1:

        print(query[0])
        return False

    data = {'disc_id': disc_id, 'svr_id': svr_id, 'char_name': char_name, 'class_name': class_name, 'ilvl': float(ilvl), 'class_eng': class_eng}
    roster_db.insert_one(data)
    return True
'''

def only_letters_and_spaces(string: str) -> bool:
    '''
    Check if string consists only of letters and white spaces

    -PARAMS-
    string: string to be evaluated
    return: True if string consists of only letters and white spaces. False otherwise
    '''
    return all(char.isalpha() or char.isspace() for char in string)

def valid_add_inputs(message: str) -> bool:
    '''
    Checks whether the user follows the correct syntax for $add operator

    -PARAMS-
    message: string with the operator $add in front
    return: True if user follows syntax rules. False otherwise 
    '''
    lst = [message.split(',')[i].strip() for i in range(len(message.split(',')))]
    return len(lst) == 4 and\
           lst[0].isalpha() and\
           only_letters_and_spaces(lst[1]) and\
           lst[3].replace('.', '', 1).isdigit() and\
           only_letters_and_spaces(lst[2].replace(':', '')) and\
           lst[1].title() in la_data.classes.keys() and\
           lst[2].title() in la_data.classes[f'{lst[1].title()}']

def query_length(query) -> int:
    '''
    Returns the length (number of data points) of the query.

    -PARAMS-
    query: the query to be counted
    return: the length of the query
    '''
    count = 0
    for x in query:
        count += 1
    return count

def display_roster(disc_id: str, svr_id: str, user_message: str) -> str:
    '''
    Displays entire roster info for the specified user.
    If no user is specified, displays the requester's entire roster.

    -PARAMS-
    svr_id: server id. A string of numbers
    disc_id: Discord id. a string of numbers
    user_message: message stringe with the $roster operator. Syntax must be $roster <OPTIONAL @discord_user>
    return: formatted roster string to be sent to the discord client
    '''
    if len(user_message.strip().split()) == 1:
        other_id = user_message.split()[0][2:-1]
        return format_display_roster(other_id, svr_id)

    return format_display_roster(disc_id, svr_id)

def format_display_roster(disc_id: str, svr_id: str) -> str:
    '''
    Helper function for display_roster
    Formats the roster string to be sent to discord client

    -PARAMS-
    svr_id: server id. A string of numbers
    disc_id: Discord id. a string of numbers
    return: formatted roster string to be sent to the discord client sorted by descending ilvl
    '''
    query = roster_db.find({'svr_id': svr_id, 'disc_id': disc_id}).sort('ilvl', -1).sort('ilvl', -1)
    str = ''
    if query_length(query) == 0:
        return str
    query = roster_db.find({'svr_id': svr_id, 'disc_id': disc_id}).sort('ilvl', -1).sort('ilvl', -1)
    for char in query:
        str += f"Character name: {char['char_name']}\n"\
               f"             -Class: {char['class_name']}\n"\
               f"             -Class engraving: {char['class_eng']}\n"\
               f"             -ilvl: {float(char['ilvl'])}\n\n"

    return str

def ranking(svr_id: str) -> str:
    '''
    Returns the top 10 highest ilvl characters within the discord server

    -PARAMS-
    svr_id: server id. A string of numbers
    return: formatted ranking string to be sent to discord client
    '''
    query = roster_db.find({'svr_id': svr_id}).sort('ilvl', -1)
    str = 'Top 10 leaderboard\n\n'
    i = 0
    for char in query:
        if i >= 10:
            break
        str += f"{i+1}. Character name: {char['char_name']}\n"\
               f"                 -Class: {char['class_name']}\n"\
               f"                 -Class engraving: {char['class_eng']}\n"\
               f"                 -ilvl: {float(char['ilvl'])}\n\n"
        i += 1
    return str

def statistics(svr_id: str) -> any:
    '''
    Returns a pie chart for Class Distribution, a scatterplot for ilvl Distribution, and average ilvl for the specified discord server.

    -PARAMS-
    svr_id: server id. A string of numbers
    return: url for pie chart, url for scatterplot, average ilvl
    '''
    query = roster_db.find({'svr_id': svr_id})
    class_distribution = {
                        'Berserker': 0,
                        'Paladin': 0,
                        'Gunlancer': 0,
                        'Destroyer': 0,
                        'Striker': 0,
                        'Wardancer': 0,
                        'Scrapper': 0,
                        'Soulfist': 0,
                        'Glaivier': 0,
                        'Machinist': 0,
                        'Gunslinger': 0,
                        'Artillerist': 0,
                        'Deadeye': 0,
                        'Sharpshooter': 0,
                        'Arcanist': 0,
                        'Bard': 0,
                        'Sorceress': 0,
                        'Reaper': 0,
                        'Shadowhunter': 0,
                        'Deathblade': 0
                        }
    ilvl_distribution = {}
    avg_ilvl = 0
    total_chars = 0
    for char in query:
        class_distribution[char['class_name']] += 1
        if float(char['ilvl']) not in ilvl_distribution.keys():
            ilvl_distribution[float(char['ilvl'])] = 1
        elif float(char['ilvl']) in ilvl_distribution.keys():
            ilvl_distribution[float(char['ilvl'])] += 1
        total_chars += 1

    # Creates pie chart for class distribution
    if total_chars != 0:
        class_distn_pie_data = [x for x in class_distribution.values() if x != 0]
        class_distn_pie_label = [x for x in class_distribution.keys() if class_distribution[x] != 0]

        class_distn_chart = QuickChart()
        class_distn_chart.width, class_distn_chart.height= 300, 300
        class_distn_chart.config = {
            "type": "doughnut",
            "data":{
                "labels": class_distn_pie_label,
                "datasets": [{
                    "label": "Class Distribution",
                    "data": class_distn_pie_data
                }]
            },
            'options':{
                'plugins':{
                    'datalabels': {
                        'backgroundColor': "#ccc",
                        'font': {
                            'size':15
                        }
                    }
                }
            }
        }

    # Creates scatterplot for ilvl disribution
    ilvl_data = [{'x': i[0], 'y': i[1]} for i in ilvl_distribution.items()]
    ilvl_distn_scat = QuickChart()
    ilvl_distn_scat.config = {
        "type": "scatter",
        "data":{
            'label': '',
            'datasets': [{
                "label": 'ilvl Distribution',
                "data": ilvl_data
            }]
        },
        'options':{
            'scales':{
                'yAxes':[{
                    'ticks':{
                        'stepSize': 1,
                        'beginAtZero': True
                    }
                }]
            }
        }
    }

    # Calculates average ilvl
    avg_ilvl = round(sum([x[0] * x[1] for x in ilvl_distribution.items()]) / total_chars, 2)

    return class_distn_chart.get_url(), ilvl_distn_scat.get_url(), avg_ilvl

def overview(svr_id: str) -> str:
    '''
    Displays everyone's roster sorted by ilvl in descending order

    -PARAMS-
    svr_id: server id. A string of numbers
    return: formatted string of all rosters to be sent to discord client
    '''
    query = roster_db.find({'svr_id': svr_id}).sort('ilvl', -1)
    str = ''
    i = 0
    for char in query:
        str += f"{i+1}. Character name: {char['char_name']}\n"\
               f"                 -Class: {char['class_name']}\n"\
               f"                 -Class engraving: {char['class_eng']}\n"\
               f"                 -ilvl: {float(char['ilvl'])}\n\n"
        i += 1

    return str

def update(svr_id: str, disc_id: str, user_message: str) -> bool:
    '''
    Updates an entry 

    -PARAMS-
    svr_id: server id. A string of numbers
    disc_id: Discord id. a string of numbers
    user_message: message stringe with the $roster operator. Syntax must be $roster <character name>, <OPTIONS name OR class OR ilvl OR engraving>, <updated info>
    return: True if successfully updated. False otherwise
    '''
    if len(user_message.split(',')) != 3:
        return False

    char_name, update_key, new = user_message.split(',')[0].strip().title(), user_message.split(',')[1].strip().lower(), user_message.split(',')[2].strip().lower()
    query = roster_db.find({'svr_id': svr_id, 'disc_id': disc_id, 'char_name': char_name})

    if query_length(query) == 0 or\
       (update_key not in convert_keys.keys()) or\
       (update_key == 'name' and not new.isalpha()) or\
       (update_key == 'class' and new.title() not in la_data.classes.keys()) or\
       (update_key == 'ilvl' and not new.replace('.', '', 1).isdigit()) or\
       (update_key == 'engraving' and new.title() not in la_data.eng):
        return False
    
    query = roster_db.find()
    if update_key in ['name', 'class', 'engraving']:
        roster_db.update_one({'svr_id': svr_id, 'disc_id': disc_id, 'char_name': char_name}, {'$set': {f'{convert_keys[update_key]}': new.title()}})
        return True
    
    roster_db.update_one({'svr_id': svr_id, 'disc_id': disc_id, 'char_name': char_name}, {'$set': {f'{convert_keys[update_key]}': float(new)}})
    return True

def delete(svr_id: str, disc_id: str, user_message: str) -> bool:
    query = roster_db.find({'svr_id': svr_id, 'disc_id': disc_id, 'char_name': user_message.strip().title()})
    if query_length(query) == 0:
        return False
    roster_db.delete_one({'svr_id': svr_id, 'disc_id': disc_id, 'char_name': user_message.strip().title()})
    return True