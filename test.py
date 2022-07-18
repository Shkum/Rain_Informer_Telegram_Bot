from Weather import Weather

a = Weather()

print(a.get_location())

a = a.check_weather()

print(a[0])
print(*a[1])
