from app.core.database import SessionLocal
from app.models import Building, Activity, Organization

db = SessionLocal()

food = Activity(name="Еда")
meat = Activity(name="Мясная продукция", parent=food)
milk = Activity(name="Молочная продукция", parent=food)

b1 = Building(
    address="г. Москва, ул. Ленина 1",
    latitude=55.7558,
    longitude=37.6176
)

org = Organization(
    name="ООО Рога и Копыта",
    phones="2-222-222,3-333-333",
    building=b1,
    activities=[meat, milk]
)

db.add_all([food, meat, milk, b1, org])
db.commit()
