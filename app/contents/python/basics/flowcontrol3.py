for i in range(3):
    print(i)


persons = ['Mike', 'Nancy', 'Tim']
for i, person in enumerate(persons):
    print('{0}: {1}'.format(i, person))


fruits_prices = {
    'apple': 200,
    'grape': 300
}
for key, value in fruits_prices.items():
    print(key, value)