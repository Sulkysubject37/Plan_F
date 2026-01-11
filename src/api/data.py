from typing import List, Optional
from pydantic import BaseModel

class RaceResult(BaseModel):
    position: int
    driver: str
    team: str
    time: str

class GrandPrix(BaseModel):
    round: int
    name: str
    location: str
    date: str
    circuit_image: str
    is_completed: bool
    winner: Optional[str] = None
    ferrari_result: Optional[str] = None

# 2026 Calendar Data
# Dates are Race Day (Sunday, except Las Vegas which is Saturday)
CALENDAR_2026 = [
    GrandPrix(
        round=1,
        name="Australian Grand Prix",
        location="Melbourne",
        date="2026-03-08",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Australia%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=2,
        name="Chinese Grand Prix",
        location="Shanghai",
        date="2026-03-15",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/China%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=3,
        name="Japanese Grand Prix",
        location="Suzuka",
        date="2026-03-29",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Japan%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=4,
        name="Bahrain Grand Prix",
        location="Sakhir",
        date="2026-04-12",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Bahrain%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=5,
        name="Saudi Arabian Grand Prix",
        location="Jeddah",
        date="2026-04-19",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Saudi%20Arabia%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=6,
        name="Miami Grand Prix",
        location="Miami",
        date="2026-05-03",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Miami%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=7,
        name="Canadian Grand Prix",
        location="Montreal",
        date="2026-05-24",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Canada%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=8,
        name="Monaco Grand Prix",
        location="Monte Carlo",
        date="2026-06-07",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Monaco%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=9,
        name="Spanish Grand Prix",
        location="Barcelona",
        date="2026-06-14",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Spain%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=10,
        name="Austrian Grand Prix",
        location="Spielberg",
        date="2026-06-28",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Austria%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=11,
        name="British Grand Prix",
        location="Silverstone",
        date="2026-07-05",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Great%20Britain%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=12,
        name="Belgian Grand Prix",
        location="Spa-Francorchamps",
        date="2026-07-19",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Belgium%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=13,
        name="Hungarian Grand Prix",
        location="Budapest",
        date="2026-07-26",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Hungary%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=14,
        name="Dutch Grand Prix",
        location="Zandvoort",
        date="2026-08-23",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Netherlands%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=15,
        name="Italian Grand Prix",
        location="Monza",
        date="2026-09-06",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Italy%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=16,
        name="Spanish Grand Prix",
        location="Madrid",
        date="2026-09-13",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Spain%20carbon.png.transform/2col/image.png", 
        is_completed=False
    ),
    GrandPrix(
        round=17,
        name="Azerbaijan Grand Prix",
        location="Baku",
        date="2026-09-27",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Azerbaijan%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=18,
        name="Singapore Grand Prix",
        location="Marina Bay",
        date="2026-10-11",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Singapore%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=19,
        name="United States Grand Prix",
        location="Austin",
        date="2026-10-25",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/USA%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=20,
        name="Mexico City Grand Prix",
        location="Mexico City",
        date="2026-11-01",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Mexico%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=21,
        name="São Paulo Grand Prix",
        location="São Paulo",
        date="2026-11-08",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Brazil%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=22,
        name="Las Vegas Grand Prix",
        location="Las Vegas",
        date="2026-11-21",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Las%20Vegas%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=23,
        name="Qatar Grand Prix",
        location="Lusail",
        date="2026-11-29",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Qatar%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=24,
        name="Abu Dhabi Grand Prix",
        location="Yas Marina",
        date="2026-12-06",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Abu%20Dhabi%20carbon.png.transform/2col/image.png",
        is_completed=False
    )
]