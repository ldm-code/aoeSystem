from datetime import datetime, timedelta
def calcular_data_transporte():
    agora = datetime.now()
    data = agora.date()

    if agora.hour >= 17:
        data += timedelta(days=1)

    if data.weekday() == 5:
        data += timedelta(days=2)
    elif data.weekday() == 6:
        data += timedelta(days=1)

    return data