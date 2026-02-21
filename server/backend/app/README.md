# Instructions

1. CD into backend
``` cd backend\app```

2. Create a venv (in \backend)
``` python -m venv venv```

3. Activate venv
```venv\scripts\activate```

4. Install dependencies
``` pip install -r requirements.txt```
or
```pip install fastapi[standard]```

5. Run main.py
``` fastapi dev app\main.py```


Go to ```http://localhost:8000/```
If it returns "Food Analyzer running" then you are good to go, if not, then delete venv folder and try the steps again.

After ensuring the main is running, you can go to ```http://localhost:8000/docs``` to read the api docs, and test them.