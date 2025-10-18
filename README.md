# chatbot-fastapi-auth
Chatbot API with FastAPI, JWT Auth, DB, and AWS  This project is a production-ready AI chatbot backend built with FastAPI. It integrates authentication, database persistence, and AWS logging to provide a secure, scalable, and extensible chatbot service.


project_root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── auth.py
│   │   └── openai_client.py
│   │   └── s3_client.py        
│   ├── models/
│   │   ├── user.py
│   │   └── message.py
│   │   └── session.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── history.py
│   │   └── admin.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── message_schema.py
│   ├── database.py
├── .env
├── requirements.txt
├── README.md
└── Architecture.png
