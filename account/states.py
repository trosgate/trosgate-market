# from django.core.management import call_command
# from django.core.management.base import BaseCommand
# from account . models import Country, State

# class Command(BaseCommand):
#     help = "this creates and maps initial states to their related countries"
    
#     def handle(self, *args, **kwargs):

#       State.objects.all().delete()
#       # country_names =[
#       #   "United States", "United Kingdom", "Ghana", "Algeria", "India"
#       # ]


#       # if not Country.objects.count():
#       #   for country_name in country_names:
#       #     Country.objects.create(name=country_name)

#     # db field for United states      
#       us_country = Country.objects.get(name="United States")

#       us_states =[
#         "Alabama", "Alaska", "Arizona", "California", "Ohio", "Oregon"
#       ]

#       for us_state in us_states:
#           State.objects.create(name=us_state, country=us_country)

#     # db field for United Kingdom
#       uk_country = Country.objects.get(name="United Kingdom")

#       uk_states =[
#         "Aberdeen", "Bournemouth", "Bath And North East Somerset", "Belfast", "Brighton And Hove"
#       ]

#       for uk_state in uk_states:
#           State.objects.create(name=uk_state, country=uk_country)

#     # db field for Ghana
#       gh_country = Country.objects.get(name="Ghana")

#       gh_states =[
#         "Greater Accra", "Central", "Northern", "Upper West", "Upper East"
#       ]

#       for gh_state in gh_states:
#           State.objects.create(name=gh_state, country=gh_country)

#     # db field for Ghana
#       al_country = Country.objects.get(name="Algeria")

#       al_states =[
#         "Algio", "Al", "Etonio"
#       ]

#       for al_state in al_states:
#           State.objects.create(name=al_state, country=al_country)

#     # db field for Ghana
#       in_country = Country.objects.get(name="India")

#       in_states =[
#         "Delhi", "Waldin", "Mumbai"
#       ]

#       for in_state in in_states:
#           State.objects.create(name=in_state, country=in_country)















