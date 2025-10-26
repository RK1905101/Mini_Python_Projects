import json
import sqlite3
import logging


def get_json(file):
    try:
        with open(file, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Unexpected Error while getting JSON file {file}: {e}")
        return {}

def create_table(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            url TEXT,
            web_site TEXT,
            domain TEXT,
            location TEXT,
            number_of_salaries INTEGER,
            average_age INTEGER,
            offers INTEGER,
            all_offers TEXT,
            spontaneous_application TEXT
        );
    ''')
    conn.commit()
    conn.close()

class Company :
    def __init__(self,
                 name,
                 url,
                 web_site,
                 domain,
                 location,
                 number_salaries,
                 average_age,
                 offers,
                 all_offers,
                 spontaneous_application):

        self.name = name
        self.url_wtj = url
        self.url_web_site = web_site
        self.domain = domain
        self.location = location
        self.number_of_salaries = number_salaries # int(number_salaries) if str(number_salaries).isdigit() else None
        self.avg_age = average_age #int(average_age.split(' ')[0]) if str(average_age).split(' ')[0].isdigit() else None
        self.offers = offers # int(offers.split(' ')[0]) if offers.split(' ')[0].isdigit() else 1 if spontaneous_application == "Oui" else 0
        self.all_offers = all_offers
        self.spontane = spontaneous_application

    def show_company(self):
        print(self.__repr__())

    def formated_data(self):
        return {
            self.name:
            {
            "Domain": self.domain,
            "Location": self.location,
            "Web Site": self.url_web_site,
            "Number of Salaries": self.number_of_salaries,
            "URL ": self.url_wtj,
            "Offers Number" : self.offers,
                "Offers List" : [self.all_offers],
            "Spontaneous application" : self.spontane,
            "Average Age": self.avg_age
            }
        }

    def __repr__(self):
        return (f"Company Name: {self.name}\n"
            f"URL: {self.url_wtj}\n"
            f"Website: {self.url_web_site}\n"
            f"Domain: {self.domain}\n"
            f"Location: {self.location}\n"
            f"Offers Number : {self.offers}\n"
            f"Spontaneous Application : {self.spontane}\n"
            f"Number of Employees: {self.number_of_salaries}\n"
            f"Average Age: {self.avg_age}\n"
            f"Spontaneous Application: {self.spontane}\n")

    def save_data_to_json(self, file):
        data = get_json(file)
        new_value = data | self.formated_data()
        with open(file, "w", encoding="utf-8") as f:
            json.dump(new_value,f,ensure_ascii=False, indent=4)

    def save_one_to_sqlite(self, db):
        create_table(db)
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                self.save_to_sqlite(cursor)
                conn.commit()
        except sqlite3.Error as e:
            print(f"[SQLite] Error while saving {self.name} : {e}")

    def save_to_sqlite(self, cursor):
        try:
            # normaliser la valeur web_site pour ne pas insérer "N/A" ou chaîne vide
            web_site_val = None if self.url_web_site in (None, "", "N/A") else self.url_web_site

            cursor.execute('''
                INSERT INTO companies (
                    name, url, web_site, domain, location,
                    number_of_salaries, average_age, offers, all_offers,
                    spontaneous_application
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    url = excluded.url,
                    web_site = CASE
                        WHEN excluded.web_site IS NOT NULL AND excluded.web_site != '' AND excluded.web_site != 'N/A'
                        THEN excluded.web_site
                        ELSE companies.web_site
                    END,
                    domain = excluded.domain,
                    location = excluded.location,
                    number_of_salaries = excluded.number_of_salaries,
                    average_age = excluded.average_age,
                    offers = excluded.offers,
                    all_offers = excluded.all_offers,
                    spontaneous_application = excluded.spontaneous_application
            ''', (
                self.name,
                self.url_wtj,
                web_site_val,
                self.domain,
                self.location,
                self.number_of_salaries,
                self.avg_age,
                self.offers,
                json.dumps(self.all_offers, ensure_ascii=False),
                self.spontane
            ))
        except Exception as e:
            print(f"[SQLite] Error while saving {self.name} : {e}")

