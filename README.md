1. Create a GitHub repo with these files:
   - main.py
   - requirements.txt
   - Dockerfile
   - .env.example
   - README.md

2. Push to GitHub.

3. On Railway:
   - Create a new project -> Deploy from GitHub -> select your repo.
   - Under Settings (Variables) add:
       API_ID, API_HASH, STRING_SESSION, OWNER_ID (optional), DEFAULT_VOLUME
   - Railway will build the Dockerfile automatically.
   - Start the service (it will run the CMD from Dockerfile).
  
     
https://www.heroku.com/deploy?template=https://github.com/PARIMUSIC/TEST 
