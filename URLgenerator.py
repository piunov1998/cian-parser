base_url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&p={}'

def generate_url(page: int) -> str:
    return base_url.format(page)


# &room1=1
# &room2=1
# &room3=1
# &room4=1
# &room5=1
# &room6=1 - 6 and more
# &room7=1 - free planing
# &room9=1 - studio