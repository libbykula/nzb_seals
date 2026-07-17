import math 

zone_coord_0 = 700
zone_coord_1 = 191

# zone_coord_0 = 1761
# zone_coord_1 = 1348
# pr = 0.5
# pr = 0.25
pr = 0.002777777777777778
div = round(1/pr)
# print(exponent)

# x = (zone_coord_0 - (zone_coord_0 % (4**exponent)))//(4**exponent)
# y = (zone_coord_1 - (zone_coord_1 % (4**exponent)))//(4**exponent)


x = zone_coord_0 //div
y = zone_coord_1//div
print(x, y)

# what if pr = 1/16?

