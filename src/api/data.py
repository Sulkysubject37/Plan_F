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

# 2025 Calendar Data (Official)
CALENDAR_2025 = [
    GrandPrix(
        round=1,
        name="Australian Grand Prix",
        location="Melbourne",
        date="2025-03-16",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Australia%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=2,
        name="Chinese Grand Prix",
        location="Shanghai",
        date="2025-03-23",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/China%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=3,
        name="Japanese Grand Prix",
        location="Suzuka",
        date="2025-04-06",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Japan%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=4,
        name="Bahrain Grand Prix",
        location="Sakhir",
        date="2025-04-13",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Bahrain%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=5,
        name="Saudi Arabian Grand Prix",
        location="Jeddah",
        date="2025-04-20",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Saudi%20Arabia%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=6,
        name="Miami Grand Prix",
        location="Miami",
        date="2025-05-04",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Miami%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=7,
        name="Emilia Romagna Grand Prix",
        location="Imola",
        date="2025-05-18",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Emilia%20Romagna%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=8,
        name="Monaco Grand Prix",
        location="Monte Carlo",
        date="2025-05-25",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Monaco%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=9,
        name="Spanish Grand Prix",
        location="Barcelona",
        date="2025-06-01",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Spain%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=10,
        name="Canadian Grand Prix",
        location="Montreal",
        date="2025-06-15",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Canada%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=11,
        name="Austrian Grand Prix",
        location="Spielberg",
        date="2025-06-29",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Austria%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=12,
        name="British Grand Prix",
        location="Silverstone",
        date="2025-07-06",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Great%20Britain%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=13,
        name="Belgian Grand Prix",
        location="Spa-Francorchamps",
        date="2025-07-27",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Belgium%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=14,
        name="Hungarian Grand Prix",
        location="Budapest",
        date="2025-08-03",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Hungary%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=15,
        name="Dutch Grand Prix",
        location="Zandvoort",
        date="2025-08-31",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Netherlands%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=16,
        name="Italian Grand Prix",
        location="Monza",
        date="2025-09-07",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Italy%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=17,
        name="Azerbaijan Grand Prix",
        location="Baku",
        date="2025-09-21",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Azerbaijan%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=18,
        name="Singapore Grand Prix",
        location="Marina Bay",
        date="2025-10-05",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Singapore%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=19,
        name="United States Grand Prix",
        location="Austin",
        date="2025-10-19",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/USA%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=20,
        name="Mexico City Grand Prix",
        location="Mexico City",
        date="2025-10-26",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Mexico%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=21,
        name="São Paulo Grand Prix",
        location="São Paulo",
        date="2025-11-09",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245032/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Brazil%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=22,
        name="Las Vegas Grand Prix",
        location="Las Vegas",
        date="2025-11-22",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Las%20Vegas%20carbon.png.transform/2col/image.png",
        is_completed=True
    ),
    GrandPrix(
        round=23,
        name="Qatar Grand Prix",
        location="Lusail",
        date="2025-11-30",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245034/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Qatar%20carbon.png.transform/2col/image.png",
        is_completed=False
    ),
    GrandPrix(
        round=24,
        name="Abu Dhabi Grand Prix",
        location="Yas Marina",
        date="2025-12-07",
        circuit_image="https://media.formula1.com/image/upload/f_auto/q_auto/v1677245035/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Abu%20Dhabi%20carbon.png.transform/2col/image.png",
        is_completed=False
    )
]
