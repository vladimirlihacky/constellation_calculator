from datetime import datetime
import time 
from typing import Union

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from constellations import Constellations

def str_to_hr(utc_time):
    utc_date = datetime.strptime(utc_time, "%Y-%m-%d")

    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }

    formatted = f"{utc_date.day} {months[utc_date.month]} {utc_date.year} года"

    return formatted

def utc_to_hr(utc_time):
    utc_date = utc_time

    if utc_time is str: 
        utc_date = datetime.strptime(utc_time, "%Y-%m-%d")

    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }

    formatted = f"{utc_date.day} {months[utc_date.month]} {utc_date.year} года"
    return formatted

templates = Jinja2Templates("templates")
templates.env.filters['utc_to_hr'] = utc_to_hr

constellations = Constellations('./constellations.json')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse(
        "constellations_all.html",
        {
            "request": request, 
            "constellations": constellations.find_all(),
            "title": "Все созвездия"
        }
    )

@app.get("/constellations/all")
async def get_all_constellations(request: Request):
    return templates.TemplateResponse(
        "constellations_all.html",
        {
            "request": request, 
            "constellations": constellations.find_all(),
            "title": "Все созвездия"
        }
    )

@app.get("/constellations/at")
async def get_all_constellations(request: Request, at):
    return templates.TemplateResponse(
        "constellations_at.html",
        {
            "request": request, 
            "date": at,
            "title": f'Созвездия, видимые {str_to_hr(at)}',
            "constellations": constellations.find_visible_at(datetime.strptime(at, "%Y-%m-%d"))
        }
    )

@app.get("/constellations/now")
async def get_all_constellations(request: Request):
    return templates.TemplateResponse(
        "constellations_at.html",
        {
            "request": request, 
            "date": datetime.now(),
            "title": f'Созвездия, видимые {utc_to_hr(datetime.now())}',
            "constellations": constellations.find_visible_at(datetime.now())
        }
    )

@app.get("/api/constellations/{id}")
def get_constellation_by_id(id):
    return constellations.find_by_id(id)

@app.get("/constellations/{id}")
async def get_constellation_by_id(request: Request, id):
    return templates.TemplateResponse(
        "constellation.html",
        {
            "request": request, 
            "constellation": constellations.find_by_id(id)
        }
    )

@app.get("/notifications")
async def get_notifications(request: Request):
    return templates.TemplateResponse(
        "notifications.html",
        {
            "request": request
        }
    )