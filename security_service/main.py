import sys
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from security_service import models, schemas, crud, auth, database  # Используем абсолютный импорт

# Добавляем путь к корневой директории проекта в sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

app = FastAPI()

# Подключение к базе данных при старте приложения
@app.on_event("startup")
def startup_event():
    database.Base.metadata.create_all(bind=database.engine)

# Функция для получения экземпляра сессии базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Регистрация пользователя
@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# Логин пользователя
@app.post("/login/")
def login_user(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Получение информации о пользователе
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user
