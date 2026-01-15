from app.core.database import SessionLocal
from app.models import Building, Activity, Organization

db = SessionLocal()

# Activities (max depth = 3)
food = Activity(name="Еда")
meat = Activity(name="Мясная продукция", parent=food)
milk = Activity(name="Молочная продукция", parent=food)

auto = Activity(name="Автомобили")
trucks = Activity(name="Грузовые", parent=auto)
cars = Activity(name="Легковые", parent=auto)
parts = Activity(name="Запчасти", parent=cars)
accessories = Activity(name="Аксессуары", parent=cars)

services = Activity(name="Услуги")
repair = Activity(name="Ремонт", parent=services)
cleaning = Activity(name="Клининг", parent=services)

# Buildings (around Moscow + nearby cities)
b_msk_1 = Building(
    address="г. Москва, ул. Ленина 1, офис 3",
    latitude=55.7558,
    longitude=37.6176,
)
b_msk_2 = Building(
    address="г. Москва, пр-т Мира 101",
    latitude=55.8245,
    longitude=37.6383,
)
b_msk_3 = Building(
    address="г. Москва, ул. Блюхера 32/1",
    latitude=55.7386,
    longitude=37.6021,
)
b_khimki = Building(
    address="г. Химки, ул. Московская 12",
    latitude=55.8970,
    longitude=37.4297,
)
b_odintsovo = Building(
    address="г. Одинцово, ул. Маршала Жукова 7",
    latitude=55.6770,
    longitude=37.2770,
)
b_balashikha = Building(
    address="г. Балашиха, пр-т Ленина 25",
    latitude=55.7964,
    longitude=37.9382,
)

# Organizations
orgs = [
    Organization(
        name="ООО Рога и Копыта",
        phones="2-222-222,3-333-333,8-923-666-13-13",
        building=b_msk_1,
        activities=[meat, milk],
    ),
    Organization(
        name="ИП Молочный Дом",
        phones="8-900-111-11-11",
        building=b_msk_1,
        activities=[milk],
    ),
    Organization(
        name="ООО Мясной Двор",
        phones="8-900-222-22-22,8-900-333-33-33",
        building=b_msk_2,
        activities=[meat],
    ),
    Organization(
        name="АО АвтоМир",
        phones="8-495-123-45-67",
        building=b_msk_2,
        activities=[auto],
    ),
    Organization(
        name="ООО ГрузСервис",
        phones="8-495-765-43-21",
        building=b_khimki,
        activities=[trucks],
    ),
    Organization(
        name="ООО ЛегкоАвто",
        phones="8-495-000-00-01",
        building=b_msk_3,
        activities=[cars],
    ),
    Organization(
        name="Мастер АвтоЗапчасти",
        phones="8-495-000-00-02",
        building=b_odintsovo,
        activities=[parts],
    ),
    Organization(
        name="АвтоАксессуар",
        phones="8-495-000-00-03",
        building=b_balashikha,
        activities=[accessories],
    ),
    Organization(
        name="Сервис Профи",
        phones="8-495-555-00-01",
        building=b_msk_3,
        activities=[repair],
    ),
    Organization(
        name="Чистый Город",
        phones="8-495-555-00-02",
        building=b_khimki,
        activities=[cleaning],
    ),
    Organization(
        name="ЕдаМаркет",
        phones="8-495-777-77-77",
        building=b_odintsovo,
        activities=[food],
    ),
    Organization(
        name="Молоко и Мясо",
        phones="8-495-888-88-88",
        building=b_balashikha,
        activities=[food, meat, milk],
    ),
]

db.add_all(
    [
        food,
        meat,
        milk,
        auto,
        trucks,
        cars,
        parts,
        accessories,
        services,
        repair,
        cleaning,
        b_msk_1,
        b_msk_2,
        b_msk_3,
        b_khimki,
        b_odintsovo,
        b_balashikha,
        *orgs,
    ]
)
db.commit()
