from fastapi import FastAPI, Request #, Depends, HTTPException, status ,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.security import APIKeyHeader
from app.database import models
from app.database.database import engine
from app.routers import routerAgents, routerListener
from app.routers import routerOrganizations
from app.routers import routerTickets
from app.routers import routerAppointments 
# from auth import auth

app = FastAPI()

################## constants ####################
DESCRIPTION = """
"""
PREFIX = '/stage/movidesk/v1'

#################################################

app = FastAPI(title='Movidesk Stage', description=DESCRIPTION)
templates = Jinja2Templates(directory='template')


# def api_token(token: str=Depends(APIKeyHeader(name='Token')), 
#                 db: Session=Depends(get_db)):
#     if not token:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
#     acess_token = crud.get_user_by_token(db, token)
#     if not acess_token:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@app.on_event('startup')
def startup_event():
    models.Base.metadata.create_all(bind=engine)


# @app.get('/test', dependencies=[Depends(auth.api_token)])
# def get_test_endpoint():
    #db: Session=Depends(get_db)):
    # if not token:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # acess_token = crud.get_user_by_token(db, token)
    # if not acess_token:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    # return {'hello': 'world'}


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/logo/netcon', response_class=FileResponse)
def get_logo():
    return '.\\static\\images\\net-logo.png'


app.include_router(routerTickets.router, prefix=PREFIX)
app.include_router(routerOrganizations.router, prefix=PREFIX)
app.include_router(routerAgents.router, prefix=PREFIX)
app.include_router(routerAppointments.router, prefix=PREFIX)
app.include_router(routerListener.router, prefix=PREFIX)
# app.include_router(users.router, prefix=PREFIX)