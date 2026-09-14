def bill(**prices):
    total = sum(prices.values())
    print("Total Bill: ", total)

bill(item1=100, item2=150, item3=200)