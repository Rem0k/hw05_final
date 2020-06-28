import datetime as dt


def year(request):
    cur_year = dt.datetime.today().year
    return {
        'year': cur_year
    }
