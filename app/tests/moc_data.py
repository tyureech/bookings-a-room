from datetime import datetime


MOC_DATA_USERS = [
    {
        "email": "user@example.com",
        "hashed_password": "qwertty"
    },
    {
        "email": "test@test.com",
        "hashed_password": "12345"
    },
    {
        "email": "tyureech@yandex.ru",
        "hashed_password": "$2b$12$5Nyx3DN0PwHQ4LMDkjpcuOJbY0KuReOacsKn5WbEg6Yo.phqMZ4jq"
    }
]

MOC_DATA_HOTELS = [
  {
    "name": "Гостиница Сыктывкар",
    "location": "Республика Коми, Сыктывкар, Коммунистическая улица, 67",
    "services": [
      "Wi-Fi",
      "Парковка",
      "Тренажёрный зал"
    ],
    "rooms_quantity": 55,
    "image_id": 4
  },
  {   
    "name": "Bridge Resort",
    "location": "посёлок городского типа Сириус, Фигурная улица, 45",
    "services": [
      "Wi-Fi",
      "Парковка",
      "Кондиционер в номере",
      "Тренажёрный зал"
    ],
    "rooms_quantity": 45,
    "image_id": 6,
  },
  {
    "name": "Skala",
    "location": "Республика Алтай, Майминский район, поселок Барангол, Чуйская улица 40а",
    "services": [
      "Wi-Fi",
      "Парковка"
    ],
    "rooms_quantity": 23,
    "image_id": 2,
  },
  {
    "name": "Ару-Кёль",
    "location": "Республика Алтай, Турочакский район, село Артыбаш, Телецкая улица, 44А",
    "services": [
      "Парковка"
    ],
    "rooms_quantity": 30,
    "image_id": 3,
  },
  {
    "name": "Palace",
    "location": "Республика Коми, Сыктывкар, Первомайская улица, 62",
    "services": [
      "Wi-Fi",
      "Парковка",
      "Кондиционер в номере"
    ],
    "rooms_quantity": 22,
    "image_id": 5,
  },
  {
    "name": "Cosmos Collection Altay Resort",
    "location": "Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20",
    "services": [
      "Wi-Fi",
      "Бассейн",
      "Парковка",
      "Кондиционер в номере"
    ],
    "rooms_quantity": 15,
    "image_id": 1,
  }
]

MOC_DATA_ROOMS = [
  {
    "hotel_id": 2,
    "name": "Номер на 3-х человек",
    "description": "Номер с видом на гору Тухтала.",
    "price": 4350,
    "services": [],
    "quantity": 8,
    "image_id": 10,
  },
  {
    "hotel_id": 2,
    "name": "Номер на 2-х человек",
    "description": "Номер с видом на океан.",
    "price": 4570,
    "services": [],
    "quantity": 15,
    "image_id": 9,
  },
    {
    "hotel_id": 1,
    "name": "Делюкс Плюс",
    "description": "Шикарный номер с видом на озеро",
    "price": 22450,
    "services": [
      "Бесплатный Wi‑Fi",
      "Кондиционер"
    ],
    "quantity": 10,
    "image_id": 8,
  },
  {
    "hotel_id": 1,
    "name": "Улучшенный с террасой и видом на озеро",
    "description": "Номер с видом на горы.",
    "price": 24500,
    "services": [
      "Бесплатный Wi‑Fi",
      "Кондиционер (с климат-контролем)"
    ],
    "quantity": 5,
    "image_id": 7,
  }
]

MOC_DATA_BOKINGS = [
    {
        "room_id": 1,
        "user_id": 1,
        "date_from": datetime.strptime("2012-12-12", "%Y-%m-%d").date(),
        "date_to": datetime.strptime("2012-12-13", "%Y-%m-%d").date(),
        "price": 2000,
    },
    {
        "room_id": 3,
        "user_id": 1,
        "date_from": datetime.strptime("2012-12-12", "%Y-%m-%d").date(),
        "date_to": datetime.strptime("2012-12-13", "%Y-%m-%d").date(),
        "price": 4562,
    },
    {
        "room_id": 1,
        "user_id": 2,
        "date_from": datetime.strptime("2012-12-12", "%Y-%m-%d").date(),
        "date_to": datetime.strptime("2012-12-13", "%Y-%m-%d").date(),
        "price": 2341,
    },
]

MOC_DATA_TEST_MODEL = [
    {
        "name": "Test1",
        "image_id": 1
    },
    {
        "name": "Test2",
        "image_id": 1
    },
    {
        "name": "Test3",
        "image_id": 2
    },
    {
        "name": "Test4",
        "image_id": 1
    }
]
