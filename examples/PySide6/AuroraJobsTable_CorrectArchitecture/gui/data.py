"""Static demo data for the Jobs screen (a real app would fetch this — here the
JobsLoaderWorker returns it off-thread). Colours are palette KEYS, resolved
against StatusPalette in style.json by the manager, never hard-coded here."""

# Status pills: (key, label, count). Colour comes from StatusPalette[key].
STATUSES = [
    ("pending", "Pending", 1235),
    ("scheduled", "Scheduled", 8902),
    ("travelling", "Travelling", 84),
    ("onhold", "On hold", 28),
    ("completed", "Completed", 565),
    ("external", "External", 23),
    ("inprogress", "In progress", 22),
    ("requested", "Requested", 1),
]

# Removable filter chips: (key, label, value).
FILTER_CHIPS = [
    ("status", "Status", "Pending"),
    ("jobtype", "Job type", "Standard job"),
    ("date", "Date", "01/10/21 – 08/01/21"),
]


def _row(job, amount, customer, street, town, due, sched1, sched2, who):
    return {"job": job, "invoiced": "Issued", "amount": amount, "customer": customer,
            "site": street, "site2": town, "due": due,
            "scheduled": sched1, "scheduled2": sched2, "assigned": who}


_BASE = [
    _row("Tracking job", 550, "Video Games Ltd", "55 Kendell Street",
         "Shaw, OL2 2YA", "16th Mar 21", "29/12/2020 09:30", "29/12/2020 10:30", "John Graham"),
    _row("Boiler service", 320, "Riverside Cafe", "12 Waterloo Road",
         "Stockport, SK1 3BD", "18th Mar 21", "30/12/2020 08:00", "30/12/2020 09:15", "Amara Okafor"),
    _row("Leak inspection", 145, "Northgate Homes", "8 Chapel Lane",
         "Bolton, BL1 4AF", "19th Mar 21", "31/12/2020 11:00", "31/12/2020 12:00", "Priya Nair"),
    _row("Panel install", 1240, "Bright Spark Ltd", "220 Deansgate",
         "Manchester, M3 4LX", "22nd Mar 21", "04/01/2021 13:30", "04/01/2021 16:00", "Diego Marín"),
    _row("Annual audit", 890, "Harbour Foods", "3 Quay Street",
         "Liverpool, L3 4AA", "23rd Mar 21", "05/01/2021 09:00", "05/01/2021 11:30", "John Graham"),
]

# job title -> "is this an active/green job" (drives the status dot colour)
GREEN_JOBS = {r["job"] for r in _BASE}

ROW_ACTIONS = [("view", "View job"), ("edit", "Edit"),
               ("duplicate", "Duplicate"), ("delete", "Delete")]


def sample_rows(n=14):
    return [dict(_BASE[i % len(_BASE)]) for i in range(n)]
