# GymPro

Gym management software for both admins and members. Members can book training sessions, manage parking, view and change their membership plan, and request a copy of their account data. Admins get an overview of activity across the club.

## Built With

| Layer | Technology |
|---|---|
| Desktop UI | [Electron](https://www.electronjs.org/) + [Vite](https://vitejs.dev/) + [React](https://reactjs.org/) + [TypeScript](https://www.typescriptlang.org/) |
| Styling | [Tailwind CSS v4](https://tailwindcss.com/) + [shadcn/ui](https://ui.shadcn.com/) |
| Backend services | [Python](https://www.python.org/) + [Flask](https://flask.palletsprojects.com/) + [Gunicorn](https://gunicorn.org/) |
| Database | [PostgreSQL](https://www.postgresql.org/) |
| Infrastructure | [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) |

## Architecture

The application is split into independent microservices that communicate over an internal Docker network (`gym-pro`). The frontend (nginx in production, Vite dev server in development) proxies all `/api/*` calls to the appropriate service.

```
Browser / Electron
       │
       ▼
  nginx / Vite proxy
       │
       ├─ /api/db-api/pay        → payment        :5427
       ├─ /api/db-api/           → db-api         :5431
       ├─ /api/account-mgmt/     → account-mgmt   :5320
       └─ /api/                  → membership-mod  :5211
                                         │
                                    db-api :5431
                                         │
                                   PostgreSQL :5432
```

| Service | Port | Responsibility |
|---|---|---|
| `ui-prod` | 5173 | Serves the compiled React SPA via nginx |
| `db-api` | 5431 | Direct database CRUD (users, schedule, parking, credit cards) |
| `account-mgmt` | 5320 | Granular user-account read endpoints |
| `membership-module` | 5211 | Membership status & plan changes |
| `payment` | 5427 | Card validation (Luhn), card storage, payment routing |
| `parking` | 5428 | Parking session management |
| `db` | 5432 | PostgreSQL — schema applied automatically on first boot |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- For development only: [Node.js](https://nodejs.org/) 18+ and [pnpm](https://pnpm.io/) v9

## Installation

### Linux

```bash
# 1. Clone the repository
git clone https://github.com/your-org/agile-assignment.git
cd agile-assignment

# 2. Build and start all services
docker compose up --build -d

# 3. Open the app
xdg-open http://localhost:5173
```

To stop everything:

```bash
docker compose down
```

To do a clean reset (wipes the database volume):

```bash
docker compose down -v
docker volume rm postgres_data
```

### Windows

> Requires [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) with WSL 2 backend enabled.

Open **PowerShell** or **Command Prompt**:

```powershell
# 1. Clone the repository
git clone https://github.com/your-org/agile-assignment.git
cd agile-assignment

# 2. Build and start all services
docker compose up --build -d

# 3. Open the app in your browser
start http://localhost:5173
```

To stop everything:

```powershell
docker compose down
```

To do a clean reset (wipes the database volume):

```powershell
docker compose down -v
docker volume rm postgres_data
```

## Development (local, without Docker)

```bash
cd electron-ui

# Install dependencies (pnpm v9 required — see note below)
pnpm install

# Start Vite dev server (proxies API calls to locally-running services)
pnpm dev

# Run as Electron desktop app
pnpm dev:electron
```

> **Note:** The lockfile requires **pnpm v9**. If you have a different version installed, run `npm install -g pnpm@9` first.

The Vite dev server proxies are pre-configured in `vite.config.ts`. You will need the backend services running (via Docker or manually) for API calls to work.

## Usage

1. Navigate to `http://localhost:5173` (or launch the Electron app).
2. Log in with the username `debug_user` to create/retrieve the built-in test account automatically.
3. Use the sidebar to navigate between pages:

| Page | What you can do |
|---|---|
| **Home** | View your session attendance charts (area + radar) |
| **Sessions** | See your scheduled sessions; book a new session |
| **Membership** | View current plan; upgrade/change by entering card details |
| **Parking** | Register a parking session; view history |
| **Account Options** | Download your data as a `.txt` file; delete your account |

## Diagrams

Design artefacts are in the [`diagrams/`](diagrams/) folder:

- Entity Relationship Diagram
- Module Diagram
- Use Case Diagram
- Activity Diagram
- Sitemap
- Scrum board snapshots

## License

Distributed under the terms of the [LICENSE](LICENSE) file in this repository.
