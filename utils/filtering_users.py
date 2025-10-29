import pandas as pd
from typing import Any
import datetime

path = r'C:\Users\Анастасия\OneDrive\Desktop\Список пользователей.csv'
df = pd.read_csv(path, delimiter=',')

def years():
    # Делим по годам
    df['Регист.'] = pd.to_datetime(df['Регист.'], errors='coerce')
    df['Год регистрации'] = df['Регист.'].dt.year
    years_filter = df[(df['Год регистрации'] >= 2020) & (df['Год регистрации'] <= 2025)].copy()
    return years_filter

def user_names(df_year: Any) -> list[str]:
    # Создаем список имен, присутствующих в таблице
    drivers_list = []
    for index, row in df_year.iterrows():
        full_name = row['ФИО']
        name = full_name.split()[1] if len(full_name.split()) > 1 else ''  # Проверка на наличие фамилии
        drivers_list.append({'name': name, 'birth_date': row['Дата Рождения']})
    return drivers_list

def calculate_age(birth_date: str) -> float:
    if pd.isnull(birth_date):
        return None
    s = str(birth_date).strip().split()[0]
    try:
        born = pd.to_datetime(s, errors='raise')
    except:
        return None
    today = pd.Timestamp.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def average_age(drivers_list: list[str]) -> int:
    # Расчет среднего возраста для женщин и мужчин
    ages = {'woman': [], 'man': []}

    for driver in drivers_list:
        age = calculate_age(driver['birth_date'])
        if age is not None:
            if driver['name'] and driver['name'][-1].lower() in ['a', 'я', 'ь']:
                ages['woman'].append(age)
            else:
                ages['man'].append(age)

    average_ages = {}
    for gender, age_list in ages.items():
        if age_list:  # Проверяем, есть ли данные для данного пола
            average_ages[gender] = sum(age_list) / len(age_list)
        else:
            average_ages[gender] = "Нет данных"

    return average_ages

def gender_ratio(drivers_list: list[str]) -> Any:
    # Кол-во пользователей/женщин/мужчин
    woman = 0
    man = 0
    users = 0
    for driver in drivers_list:
        name = driver['name']
        if name and name[-1].lower() in ['a', 'я', 'ь']:  # Проверка на наличие имени
            woman += 1
        else:
            man += 1
        users += 1

    if users == 0:
        return "Нет данных"

    return {
        'total_users': users,
        'women': woman,
        'men': man,
        'women_ratio': (woman / users) * 100,
        'men_ratio': (man / users) * 100
    }

def split_statistics() -> Any:
    # Кол-во пользователей по годам
    years_data = years()
    if years_data.empty:
        return "Нет данных за указанный период"

    grouped = years_data.groupby('Год регистрации')
    results = ''

    for year, group in grouped:
        names = user_names(group)
        gender_stats = gender_ratio(names)
        age_stats = average_age(names)

        results += f"Год {year}:\n"
        results += f" Всего пользователей: {gender_stats['total_users']}; "
        results += f"Женщин: {gender_stats['women']}, процентное соотношение: {gender_stats['women_ratio']:.2f}%; "
        results += f"Мужчин: {gender_stats['men']}, процентное соотношение: {gender_stats['men_ratio']:.2f}%;\n"

        results += f" Средний возраст женщин: {age_stats['woman'] if isinstance(age_stats['woman'], str) else age_stats['woman']:.0f}, "
        results += f"Средний возраст мужчин: {age_stats['man'] if isinstance(age_stats['man'], str) else age_stats['man']:.0f}\n"

    return results

print(split_statistics())