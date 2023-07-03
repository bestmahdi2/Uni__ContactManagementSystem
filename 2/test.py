import re

# address = "madonna.murazik@gmail.com"
address = "llindgren@crona.net"
# address = "yundt.earlene@hotmail.com"

if address != "":
    pattern = r'^([0-9A-Za-z]|\.|\_|\-)+[@]([0-9A-Za-z]|\_|\-|\.)+[.][A-Za-z]{2,3}$'

    if re.search(pattern, address):
        print(True)
    else:
        print(False)