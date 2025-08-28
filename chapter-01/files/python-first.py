# Первая программа аналитика данных
# Глава 1: Анализ продаж кафе

# Данные за неделю
coffee_cups = [45, 52, 38, 41, 67, 89, 73]
revenue = [13500, 15600, 11400, 12300, 20100, 26700, 21900]
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

print("🏪 Добро пожаловать в аналитику кафе!")
print("📊 Данные загружены успешно!")

# Базовая статистика  
total_cups = sum(coffee_cups)
total_revenue = sum(revenue)
average_cups = total_cups / len(coffee_cups)
average_revenue = total_revenue / len(revenue)
average_price = total_revenue / total_cups

print(f"☕ Всего продано чашек: {total_cups}")
print(f"💰 Общая выручка: {total_revenue:,} руб")
print(f"📈 Средние чашки в день: {average_cups:.1f}")
print(f"💵 Средняя выручка в день: {average_revenue:,.0f} руб")
print(f"🏷️ Средняя цена чашки: {average_price:.0f} руб")

# Находим рекордсменов
best_day_index = coffee_cups.index(max(coffee_cups))
worst_day_index = coffee_cups.index(min(coffee_cups))

print(f"🏆 Лучший день: {days[best_day_index]} ({max(coffee_cups)} чашек)")
print(f"😔 Худший день: {days[worst_day_index]} ({min(coffee_cups)} чашек)")

# Считаем разницу
difference = max(coffee_cups) - min(coffee_cups)
print(f"📊 Разница между лучшим и худшим днём: {difference} чашек")

# Создаём простой график из символов
print("\n📊 График продаж (каждый * = 10 чашек):")
for i, day in enumerate(days):
    stars = "*" * (coffee_cups[i] // 10)
    print(f"{day[:3]}: {stars} ({coffee_cups[i]})")

# Делаем простые выводы
print("\n🤔 Простые выводы:")

if max(coffee_cups) > average_cups * 1.5:
    best_day = days[best_day_index]
    print(f"• {best_day} - явно выдающийся день! Стоит изучить причины.")

weekend_sales = coffee_cups[5] + coffee_cups[6]  # Суббота + Воскресенье
weekday_sales = sum(coffee_cups[:5])  # Пн-Пт

if weekend_sales > weekday_sales / 5 * 2:
    print("• Выходные дни более прибыльны чем будни.")
else:
    print("• Будние дни стабильнее выходных.")

if average_price > 300:
    print("• Средняя цена выше 300 рублей - премиум сегмент.")
else:
    print("• Демократичные цены - массовый сегмент.")