from beanie import Document


class User(Document):
    fullname: str
    phone_number: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "phone_number": "+79858693770",
                "password": "3xt3m#",
            }
        }

    class Settings:
        name = "users"


