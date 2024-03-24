from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from Routers import auth_router, roles_router, users_router, vehicles_router


### FastAPI App ### 
app = FastAPI()

### CORS Middleware ### 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### Default Route ###
@app.get("/")
def read_root():
    return {"message": "Project Flas API"} 


# Authentication Router
app.include_router(auth_router.router)

# Roles Router
app.include_router(roles_router.router)

# Users Router
app.include_router(users_router.router)

# Vehicles Router
app.include_router(vehicles_router.router)



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            



