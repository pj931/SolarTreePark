def volt_div(r1,r2,vin):
    vout = (vin*r1)/(r1+r2)
    return round(vout,3)

print(volt_div(33000,10000,5.0))
