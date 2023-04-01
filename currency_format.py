amount = 123456458.78
thousands_separator = "."
fractional_separator = ","

currency = "${:,.2f}".format(amount)

if thousands_separator == ".":
    main_currency, fractional_currency = currency.split(".")[0], currency.split(".")[1]
    new_main_currency = main_currency.replace(",", ".")
    currency = new_main_currency + fractional_separator + fractional_currency

print(currency*100)