import csv
import random

def generate_csv(filename="onboarding_data.csv", num_rows=1000):
    positions = ["Developer", "QA", "Designer", "Manager", "DevOps"]
    equipments = ["MacBook Pro", "Dell XPS", "ThinkPad", "Monitor 27'", "Keyboard"]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["FirstName", "LastName", "Email", "Position", "EquipmentModel", "SystemAccount"])
        
        for i in range(1, num_rows + 1):
            writer.writerow([
                f"Name{i}",
                f"Surname{i}",
                f"user{i}@lviv.polytechnic.ua",
                random.choice(positions),
                random.choice(equipments),
                f"SAP_Acc_{i}"
            ])
            
    print(f"File {filename} successfully generated with {num_rows} rows.")

if __name__ == "__main__":
    generate_csv()