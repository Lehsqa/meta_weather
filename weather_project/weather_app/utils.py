from selenium import webdriver
from bs4 import BeautifulSoup
from .models import Weather
from datetime import datetime, timedelta


def update_weather():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options=options)

    url = "https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/month/"
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Находим блок с прогнозом погоды на 5 дней
    day_blocks = soup.find_all('div', attrs={'class': 'month__day fl-col-c-c'}, limit=6)
    prev_day = datetime.now().date() - timedelta(days=1)
    for day_block in day_blocks:
        # Получаем дату
        date = prev_day + timedelta(days=1)
        prev_day = date

        # Получаем температуру
        temperature = day_block.find('span', attrs={'class': 'high'}).text.strip()

        # Получаем описание погоды
        description = day_block.find('div', attrs={'class': 'month__icon'}).find('span')['data-tippy-content']

        # Проверяем, существует ли запись для этой даты
        try:
            weather = Weather.objects.get(date=date)
            weather.temperature = temperature
            weather.description = description
            weather.save()
        except Weather.DoesNotExist:
            Weather.objects.create(date=date, temperature=temperature, description=description)
