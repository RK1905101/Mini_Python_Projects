import sqlite3
import json

from Company import Company, get_json

class Companies:
    def __init__(self, companies: list[Company] ):
        self.companies = companies

    def show_companies(self):
        for company in self.companies:
            company.show_company()

    def save_companies_to_json(self, file):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump([company.formated_data() for company in self.companies], f, ensure_ascii=False, indent=4)

    def save_companies_to_sqlite(self, db):
        from Company import create_table
        create_table(db) 
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            for company in self.companies:
                company.save_to_sqlite(cursor)
            conn.commit()

    def get_companies_from_sqlite(self, db):
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM companies')
            all_companies = cursor.fetchall()

            return Companies([
                Company(
                    name=row[1],
                    url=row[2],
                    web_site=row[3],
                    domain=row[4],
                    location=row[5],
                    number_salaries=row[6],
                    average_age=row[6],
                    offers=row[7],
                    all_offers= json.loads(row[8]) if isinstance(row[8], (str, bytes, bytearray)) else row[8],
                    spontaneous_application=row[9],
                ) for row in all_companies
            ])

    def get_companies_from_json(self, file):
        all_companies = get_json(file)
        return Companies([
            Company(
                name,
                company.get("URL ", "Unknown"),
                company.get("Web Site", "Unknown"),
                company.get("Domain", "Unknown"),
                company.get("Location", "Unknown"),
                company.get("Number of Salaries", "Unknown"),
                company.get("Average Age", "Unknown"),
                company.get("Offers Number", "Unknown"),
                company.get("Offers List", "Unknown"),
                company.get("Spontaneous application", "Unknown"),
            ) for companies in all_companies for name, company in companies.items()
        ])

