from weather import weather

weather = weather.weather()

lookup = weather.lookup_by_location('Da nang')
condition = lookup.condition

print(condition.text)