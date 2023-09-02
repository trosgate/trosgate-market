from account.models import Country, State, City
import json
import csv


def default_country_state_city():
    # # INITIAL DATABASE POPULATOR STARTS
    Country.objects.all().delete()
    countries_to_create = []

    with open('./countries.csv', 'r', encoding='utf-8') as f:
        result = list(csv.DictReader(f))
        for row in result:
            country = Country(
                id=row['id'],
                name=row['name'],
                region=row['region'],
                subregion=row['subregion'],
                ordering=row['id'],
                country_code=row['iso2'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                currency_name=row['currency_name'],
                phone_code=row['phone_code'],
                currency=row['currency']
            )
            countries_to_create.append(country)

    Country.objects.bulk_create(countries_to_create)


    with open('./country_and_flag.json', 'r', encoding='utf-8') as f:
        result = json.load(f)
        for res in result:
                field = res.get('fields')
                country_code, flag = field.get('country_code'), field.get('flag')
                for country in Country.objects.all():
                    if country.country_code == country_code:
                        country.flag = flag
                        country.save()
                        
    print('Country ended')

    State.objects.all().delete()
    states_to_create = []

    with open('./states.csv', 'r', encoding='utf-8') as f:
        result = list(csv.DictReader(f))
        for row in result:
            state = State(
                id=row['id'],
                name=row['name'],
                ordering=row['id'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                state_code=row['state_code'],
                country_id=row['country_id']
            )
            states_to_create.append(state)

    State.objects.bulk_create(states_to_create)

    print('State ended')

    City.objects.all().delete()
    cities_to_create = []

    with open('./cities.csv', 'r', encoding='utf-8') as f:
        result = list(csv.DictReader(f))
        for row in result:
            city = City(
                id=row['id'],
                name=row['name'],
                ordering=row['id'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                country_id=row['country_id'],
                state_id=row['state_id'],
                wikidata=row['wikiDataId']
            )
            cities_to_create.append(city)

    City.objects.bulk_create(cities_to_create)

    print('City ended')
