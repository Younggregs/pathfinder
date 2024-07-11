ARIK_URL = "https://arikair.crane.aero/ibe/availability?tripType=ONE_WAY&depPort={origin}&arrPort={destination}&departureDate={departure_date}&returnDate=&passengerQuantities%5B0%5D%5BpassengerType%5D=ADULT&passengerQuantities%5B0%5D%5BpassengerSubType%5D=&passengerQuantities%5B0%5D%5Bquantity%5D=1&passengerQuantities%5B1%5D%5BpassengerType%5D=CHILD&passengerQuantities%5B1%5D%5BpassengerSubType%5D=&passengerQuantities%5B1%5D%5Bquantity%5D=0&passengerQuantities%5B2%5D%5BpassengerType%5D=INFANT&passengerQuantities%5B2%5D%5BpassengerSubType%5D=&passengerQuantities%5B2%5D%5Bquantity%5D=0&currency=&cabinClass=&lang=EN&nationality=&promoCode=&accountCode=&affiliateCode=&clickId=&withCalendar=&isMobileCalendar=&market=&isFFPoint=&_ga="

AIRPEACE_URL = "https://book-airpeace.crane.aero/ibe/availability?tripType=ONE_WAY&depPort={origin}&arrPort={destination}&departureDate={departure_date}%20%20%20%20%20%20%20%20&adult=1&child=0&infant=0&currency=NGN&lang=en"

IBOM_AIR_URL = "https://book-ibomair.crane.aero/ibe/availability?tripType=ONE_WAY&depPort={origin}&arrPort={destination}&departureDate={departure_date}&returnDate=&passengerQuantities%5B0%5D%5BpassengerType%5D=ADULT&passengerQuantities%5B0%5D%5BpassengerSubType%5D=&passengerQuantities%5B0%5D%5Bquantity%5D=1&passengerQuantities%5B1%5D%5BpassengerType%5D=CHILD&passengerQuantities%5B1%5D%5BpassengerSubType%5D=&passengerQuantities%5B1%5D%5Bquantity%5D=0&passengerQuantities%5B2%5D%5BpassengerType%5D=INFANT&passengerQuantities%5B2%5D%5BpassengerSubType%5D=&passengerQuantities%5B2%5D%5Bquantity%5D=0&currency=NGN&cabinClass=&lang=EN&nationality=&promoCode=&accountCode=&affiliateCode=&clickId=&withCalendar=&isMobileCalendar=&market=&isFFPoint="

NG_EAGLE_URL = "https://book-ngeagle.crane.aero/ibe/availability/?currency=NGN&lang=en&departureDate={departure_date}&returnDate=&depPort={origin}&arrPort={destination}&tripType=ONE_WAY&adult=1&child=0&infant=0"

GREEN_AFRICA_URL = "https://middleware.greenafrica.com/api/booking/getDeepLink?from={origin}&to={destination}&start={departure_date}&adults=1&child=0&session_id=NppD+fXAhDlxp9X2HjvoejpAnr4eNiXSlk0JuDFODYhdoik0JJ&infant=0&currency=NGN&cabinCode=ECO"

GREEN_AFRICA_DIRECT_LINK = "https://greenafrica.com/booking/select?origin={origin}&destination={destination}&departure={departure_date}&adt=1&chd=0&inf=0&promocode="

VALUE_JET_URL = "https://flyvaluejet.com/flight-result?requestInfo=dep:%27{origin}%27,arr:%27{destination}%27,on:%27{departure_date}%27,till:%27%27,p.a:1,p.c:0,p.i:0"

UNITED_NIGERIA_URL = "https://booking.flyunitednigeria.com/VARS/Public/CustomerPanels/requirementsBS.aspx"

MAX_URL = "https://customer2.videcom.com/MaxAir/VARS/Public/CustomerPanels/requirementsBS.aspx"

RANO_URL = "https://customer3.videcom.com/RanoAir/VARS/Public/CustomerPanels/requirementsBS.aspx"

LOCATIONS = [
    {"name": "Lagos", "code": "LOS"},
    {"name": "Abuja", "code": "ABV"},
    {"name": "Akure", "code": "AKR"},
    {"name": "Anambra", "code": "ANA"},
    {"name": "Asaba", "code": "ABB"},
    {"name": "Bauchi", "code": "BCU"},
    {"name": "Benin", "code": "BNI"},
    {"name": "Birnin Kebbi", "code": "DNBK"},
    {"name": "Calabar", "code": "CBQ"},
    {"name": "Enugu", "code": "ENU"},
    {"name": "Gombe", "code": "GMO"},
    {"name": "Ibadan", "code": "IBA"},
    {"name": "Ilorin", "code": "ILR"},
    {"name": "Kaduna", "code": "KAD"},
    {"name": "Kano", "code": "KAN"},
    {"name": "Katsina", "code": "DKA"},
    {"name": "Jos", "code": "JOS"},
    {"name": "Maiduguri", "code": "MIU"},
    {"name": "Makurdi", "code": "MDI"},
    {"name": "Owerri", "code": "QOW"},
    {"name": "Port Harcourt", "code": "PHC"},
    {"name": "Sokoto", "code": "SKO"},
    {"name": "Uyo", "code": "QUO"},
    {"name": "Warri", "code": "QRW"},
    {"name": "Yenagoa", "code": "BIA"},
    {"name": "Yola", "code": "YOL"},
    {"name": "Cotonou", "code": "COO"},
    {"name": "Douala", "code": "DLA"},
    {"name": "Banjul", "code": "BJL"},
    {"name": "Accra", "code": "ACC"},
    {"name": "Abidjan", "code": "ABJ"},
    {"name": "Monrovia", "code": "ROB"},
    {"name": "Jeddah", "code": "JED"},
    {"name": "Medina", "code": "MED"},
    {"name": "Dakar Blaise Diagne Internatio", "code": "DSS"},
    {"name": "Freetown", "code": "FNA"},
    {"name": "Johannesburg", "code": "JNB"},
    {"name": "Lome", "code": "LFW"},
    {"name": "London", "code": "LGW"},
]
