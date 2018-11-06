import urllib.request
import requests
import os
import os.path
import csv


# Global varibles
new_fn = 'new_data.csv'
old_fn = 'archive.csv'
delta_fn = 'delta.csv'


def get_conf_data():

    # SC is the event code in the Xpress Lead data
    sc = 'ACTF1118'

    # EXID is the exhibitor ID
    exid = '1894511'

    # Email for the account (AKA Michelle)
    em = 'michelle@waysidepublishing.com'

    term_id = 'D356DF7FA99849B'
    
    url = 'https://www.xpressleadpro.com/portal/public/signin/smillette@waysidepublishing.com/1894511/qualifiers'

    s = requests.Session()

    s.get(url)

    download_url = "https://www.xpressleadpro.com/portal/public/downloadbytid/1894511/D356DF7FA99849B/csv"

    with open(new_fn, 'wb') as out_file:
        data = s.get(download_url)
        out_file.write(data.content)


def get_just_new_data_from():
    # If "archive.csv" doesn't exist, that means this is the first set of data ever downloaded
    if os.path.isfile(old_fn) is not True: 
        return new_fn

    else:
        with open(delta_fn, 'a') as delta_file, open(old_fn, 'r') as old_file, open(new_fn, 'r') as new_file:
            old_file_data = csv.DictReader(old_file)
            new_file_data = csv.DictReader(new_file)

            headers = new_file_data.fieldnames

            writer = csv.DictWriter(delta_file, fieldnames=headers)
            writer.writeheader()

            for line in new_file_data:
                if line not in old_file_data:
                    writer.writerow(line)

        return delta_fn


# this method maps Xpress Lead answer's form value to the form name
def map_from_to(v, n):
    all_val = v.split('|')
    ret_val = {}

    for v in all_val:
        curr_tag_name = n.get(v)
        if curr_tag_name is not None or curr_tag_name is not '':
            ret_val[curr_tag_name] = curr_tag_name.split("_")[-1]

    return ret_val


def handle_headers(header, value):
    if header == "Level":
        level_values = {
            "High School": "426379",
            "Middle/Jr. High": "426381",
            "Elementary": "426383",
            "Elementary,Middle/Jr. High,High School": "426385",
            'Middle/Jr. High,High School': '426387',
            'Community College': '426389',
            'Adult Ed': '426391'
        }
        return level_values.get(value, '')

    if header == "Languages":
        language_values = {
            'Spanish': '359661_41981pi_359661_41981_426009',
            'French': '359661_41981pi_359661_41981_426011',
            'German': '359661_41981pi_359661_41981_426013',
            'Italian': '359661_41981pi_359661_41981_426015',
            'Latin': '359661_41981pi_359661_41981_426017',
            'Portuguese': '359661_41981pi_359661_41981_426019',
            'Mandarin': '359661_41981pi_359661_41981_426021',
            'Japanese': '359661_41981pi_359661_41981_426023',
            'Hindi': '359661_41981pi_359661_41981_426025',
            'Arabic': '359661_41981pi_359661_41981_426027',
            'Russian': '359661_41981pi_359661_41981_426029',
        }

        return map_from_to(value, language_values)

    if header == 'Email 30 day access to these programs':
        digital_values = {
            'EntreCulturas 1 - Spanish': '359661_41915pi_359661_41915_425935',
            'EntreCulturas 1a - Spanish': '359661_42103pi_359661_42103_426413',
            'EntreCulturas 1b - Spanish': '359661_42105pi_359661_42105_426415',
            'EntreCulturas 2 - Spanish': '359661_41917pi_359661_41917_425937',
            'EntreCulturas 3 - Spanish': '359661_41919pi_359661_41919_425939',
            'Tejidos': '359661_41921pi_359661_41921_425941',
            'Triangulo Aprobado': '359661_41923pi_359661_41923_425943',
            'Triangulo APreciado': '359661_42107pi_359661_42107_426417',
            'Azulejo': '359661_41925pi_359661_41925_425945',
            'APprenons': '359661_41927pi_359661_41927_425947',
            'Neue Blickwinkel': '359661_41929pi_359661_41929_425949',
            'Chiarissimo Uno': '359661_41931pi_359661_41931_425951',
            'Chiarissimo Due': '359661_41933pi_359661_41933_425953',
            'Scandite Muros': '359661_41935pi_359661_41935_425955'

        }

        return map_from_to(value, digital_values)

    if header == "Wayside is giving you these print resources now":
        print_values = {
            'EntreCultures Sampler': '359661_42115pi_359661_42115_426425',
            'EntreCulturas 1a': '359661_42117pi_359661_42117_426427',
            'EntreCulturas 1b': '359661_42119pi_359661_42119_426429',
            'EntreCulturas 1': '359661_41937pi_359661_41937_425957',
            'EntreCulturas 2': '359661_41939pi_359661_41939_425959',
            'EntreCulturas 3': '359661_41941pi_359661_41941_425961',
            'Tejidos': '359661_41943pi_359661_41943_425963',
            'Triangulo Aprobado': '359661_41945pi_359661_41945_425965',
            'Triangulo APreciado': '359661_42121pi_359661_42121_426431',
            'Azulejo': '359661_41947pi_359661_41947_425967',
            'APprenons': '359661_41949pi_359661_41949_425969',
            'Neue Blickwinkel': '359661_41951pi_359661_41951_425971',
            'Chiarissimo Uno': '359661_41953pi_359661_41953_425973',
            'Chiarissimo Due': '359661_41955pi_359661_41955_425975',
            'Scandite Muros': '359661_41957pi_359661_41957_425977',
        }
        return map_from_to(value, print_values)

    # This is actually DIGITAL TOOLS because Xpress Leads is terrible.
    if header == "The next adoption-related deadline will be":
        digital_tools_values = {
            '1 to 1': '',
            '1 to 2 or more': '',
            'Technology Cart': '',
            'Language Lab': ''
        }

        return map_from_to(value, digital_tools_values)

    # This is actually THE NEXT ADOPTION-RELATED DEADLINE WILL BE because Xpress Leads is terrible
    if header == "Digital tools in your classroom":
        deadline_values = {
            'Before 2019': '',
            'Spring 2019': '',
            'Spring 2020': '',
            'Fall 2019': ''
        }

        return map_from_to(value, deadline_values)

    if header == 'Wayside should stay in touch about':
        in_touch_values = {
            'Wayside newsletter subscription': '',
            'EntreCultures 1a 1b - French': '',
            'EntreCultures 1  - French': '',
            'EntreCultures 2 and or 3 - French': '',
            'Updates on EntreCulturas 4 - Spanish': '',
            'Learning Site Updates': '',
            'Updates on German 1, 2, 3': ''
        }

        return map_from_to(value, in_touch_values)

    # This is actually POST-ACTFL SHIPMENT REQUESTED
    if header == 'If you had your wish, Wayside would create':
        create_values = {
            'EntreCulturas 1a': '',
            'EntreCulturas 1b': '',
            'EntreCulturas 1': '',
            'EntreCulturas 2': '',
            'EntreCulturas 3': '',
            'Tejidos': '',
            'Triangulo Aprobado': '',
            'Triangulo APreciado': '',
            'Azulejo': '',
            'APprenons': '',
            'Neue Blickwinkel': '',
            'Chiarissimo Uno': '',
            'Chiarissimo Due': '',
            'Scandite Muros': ''
        }

        return map_from_to(value, create_values)

    # This is actually IF YOU HAD YOUR WISH, WAYSIDE WOULD CREATE
    if header == 'OPTIONAL Non Sales Follow Up':
        sales_values = {
            'Spanish for heritage speakers': '',
            'Elementary Spanish': '',
            'Chiarissimo Tre': '',
            'Elementary French': '',
            'French for heritage speakers': '',
            'Elementary Mandarin': '',
            '6-12 Mandarin': '',
            'A broader Latin line': ''
        }

        return map_from_to(value, sales_values)


def push_data_to(fn, url):
    with open(fn, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        tag_names = {
            'First Name': '359661_41897pi_359661_41897',
            'Last Name': '359661_41899pi_359661_41899',
            'Company': '359661_41903pi_359661_41903',
            'Street': '359661_41905pi_359661_41905',
            'Street (line 2)': '359661_41907pi_359661_41907',
            'City': '359661_41909pi_359661_41909',
            'State/Province': '359661_41911pi_359661_41911',
            'Zip Code': '359661_41913pi_359661_41913',
            'Country': '359661_42097pi_359661_42097',
            'Phone': '359661_42099pi_359661_42099',
            'Email': '359661_41901pi_359661_41901',

            'Assignment': '359661_41979pi_359661_41979',
            'Level': '359661_42101pi_359661_42101',

            'Languages': '',

            'Name of Waysider completing this form': '359661_42703pi_359661_42703',

            'Email 30 day access to these programs': '',

            'Wayside is giving you these print resources now': '',

            'The next adoption-related deadline will be': '',

            'Digital tools in your classroom': '',

            'Wayside should stay in touch about': '',

            'If you had your wish, Wayside would create': '',

            # This is actually OPTIONAL NON SALES FOLLOW UP
            'Post-ACTFL shipment requested': '359661_42705pi_359661_42705',

            # This is actually IF YOU HAD YOUR WISH, WAYSIDE WOULD CREATE
            'OPTIONAL Non Sales Follow Up': '',

            'Print': '21',
            'Ship': '22',
            'Lead_Rating': '23',
        }

        all_data = []

        for row in reader:
            data = {}
            for header in headers:
                tag_name = tag_names.get(header)
                if tag_name is not None:
                    value = row[header]
                    if header in ["Level",
                                  "Languages",
                                  "Email 30 day access to these programs",
                                  "Wayside is giving you these print resources now",
                                  "The next adoption-related deadline will be",
                                  "Digital tools in your classroom",
                                  "Wayside should stay in touch about",
                                  "If you had your wish, Wayside would create",
                                  "Post-ACTFL shipment requested",
                                  "Lead Rating"]:
                        return_value = handle_headers(header, value)
                        if isinstance(return_value, str):
                            data[tag_name] = return_value
                        else:
                            data.update(return_value)
                    else:
                        data[tag_name] = value
            all_data.append(data)

        # Enter POST request here

        for data in all_data[2:]:
            r = requests.post(url, data=data)
            print(r.status_code)


def cleanup():
    if os.path.isfile(old_fn):
        os.remove(old_fn)

    if os.path.isfile(delta_fn):
        os.remove(delta_fn)

    os.rename(new_fn, old_fn)


def main():

    # Getting fresh data
    get_conf_data()
    
    # Parsing through new data to check for duplicates between "new_data.csv" and "archive.csv" if "archive.csv" exists
    parsed_data_fn = get_just_new_data_from()
    
    # Push data to the LS and Pardot
    push_data_to(parsed_data_fn, 'http://www2.waysidepublishing.com/l/359661/2018-10-22/dn4z2b')

    # Deleting "archive.csv" and "delta.csv" if necessary, renames "new_data.csv" to "archive.csv"
    cleanup()   


main()
