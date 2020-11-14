import csv
from haversine import haversine, Unit

DATA_DIR = '../../data'
LAKES_TARGET_CSV = f'{DATA_DIR}/lakes_2015.csv'
BASE_CSV = f'{DATA_DIR}/base_dataset.csv'
OUT_FILE = f'{DATA_DIR}/nearest_lakes.csv'


def load_lakes():
    lakes = dict()
    with open(LAKES_TARGET_CSV) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lat = float(row['centr_lat'])
            lon = float(row['centr_lon'])
            hylak_id = row['Hylak_id']
            lakes[(lat, lon)] = hylak_id
    return lakes


def load_base():
    plants = dict()
    with open(BASE_CSV) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            plant_id = row['id']
            plants[(lat, lon)] = plant_id
    return plants


def match_plants_to_lakes(plants, lakes):
    matches = []
    for plant_coord, plant_id in plants.items(): 
        closest_dist, closest_lake_id = -1, -1
        for lake_coord, lake_id in lakes.items(): 
            d = haversine(plant_coord, lake_coord)
            if closest_dist == -1 or closest_dist > d:
                closest_dist = d
                closest_lake_id = lake_id
        matches.append((plant_id, closest_lake_id, closest_dist))
    return matches


def write_matches_to_csv(matches):
    out = open(OUT_FILE, 'w')
    out.write(','.join([
        'plant_id', 
        'lake_id', 
        'distance_km'
    ]) + '\n')

    for m in matches:
        out.write(','.join([
            m[0],
            m[1],
            str(m[2])
        ]) + '\n')


def main():
    plants = load_base()
    print(plants)

    # lakes = load_lakes()

    # matches = match_plants_to_lakes(plants, lakes)
    # write_matches_to_csv(matches)


if __name__ == '__main__':
    main()
