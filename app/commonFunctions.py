from datetime import date

def calculatePaymentDays(fromDate, toDate):
    return (date.fromisoformat(toDate) - date.fromisoformat(fromDate)).days