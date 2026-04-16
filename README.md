# INFO3180 VueJS and Flask Starter

## API Endpoints

### Authentication
- `POST /register` – Register a new user. Body: `{"email": "...", "password": "..."}`
- `POST /login` – Login and start session. Body: `{"email": "...", "password": "..."}`
- `POST /logout` – Logout and destroy session.
- `GET /me` – Get current user details and profile.

### Profile Management
- `GET /profile/<id>` – Get a user's profile.
- `PUT /profile` – Create or update your own profile. Body: `{"name": "...", "age": 25, "bio": "...", "location": "...", "interests": ["..."], "gender": "...", "looking_for": "...", "is_public": true}`
- `POST /profile/photo` – Upload a profile picture. Form-data: `photo: <file>`

### Matching System
- `GET /matches` – List of mutual matches.
- `GET /potential-matches` – Ranked list of potential matches based on location, age, and interests.
- `POST /like/<user_id>` – Like a user. Returns "matched" if mutual.
- `POST /pass/<user_id>` – Pass on a user.

### Messaging
- `GET /messages/<match_id>` – Get conversation history for a match.
- `POST /messages/<match_id>` – Send a message. Body: `{"content": "..."}`
- `GET /conversations` – List of all active conversations with the last message.

### Search & Discovery
- `GET /search?location=...&min_age=...&max_age=...&interests=...` – Search for users with filters.
- `GET /favorites` – List your bookmarked profiles.
- `POST /favorites/<user_id>` – Toggle bookmark for a profile.

---

This template should help get you started developing with Vue 3 on the frontend and Flask as an API on the backend.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Start Flask API

Remember to always create a virtual environment and install the packages in your requirements file

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app --debug run
```
