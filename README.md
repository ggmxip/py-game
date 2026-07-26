# Python Game Learning Roadmap 🎮

A structured **beginner-to-advanced** Python learning path built entirely through games. Each phase introduces new programming concepts by building a complete, runnable game.

## Phases

| Phase | Project | Concepts | Level |
|---|---|---|---|
| **1** | **Math Challenge** | Functions, modules, `random`/`json`, file I/O, loops, conditionals | Beginner |
| **2** | **Text-Based RPG** | OOP (classes, inheritance), `@dataclass`, save/load, game state | Early Intermediate |
| **3** | **Space Shooter** (pygame) | Third-party libraries, event loops, sprites, collision detection | Intermediate |
| **4** | **Roguelike** (tcod) | 2D grids, procedural generation, pathfinding (A*), FOV | Intermediate+ |
| **5** | **Multiplayer Quiz** | Sockets, threading, client-server architecture, protocols | Advanced |
| **6** | **Web Quiz** (FastAPI) | Async web frameworks, WebSockets, REST API, SQLite, HTML/JS | Advanced |

---

## How to Run

### Phase 1 — Math Challenge
```bash
python main.py
```
Terminal-based quiz. Answer 10 math questions per round, save high scores.

### Phase 2 — Text RPG
```bash
python phase2_text_rpg/main.py
```
Explore rooms, fight enemies, collect items, save progress. Commands: `look`, `move <dir>`, `inventory`, `use <item>`, `save`, `help`.

### Phase 3 — Space Shooter
```bash
pip install pygame
python phase3_pygame/main.py
```
Arrow keys to move, SPACE to shoot. Survive as long as you can.

### Phase 4 — Roguelike
```bash
pip install tcod
python phase4_roguelike/main.py
```
Requires `dejavu10x10_gs_tc.png` from the [tcod tutorial assets](https://github.com/HexDecimal/tcod_tutorial_assets). Turn-based dungeon crawling with procedural generation.

### Phase 5 — Multiplayer Quiz
```bash
# Terminal 1 — Server
python phase5_multiplayer/server.py

# Terminal 2 — Client
python phase5_multiplayer/client.py
```
Connect multiple clients. Answer questions and compare scores.

### Phase 6 — Web Quiz
```bash
pip install fastapi uvicorn
cd phase6_web
uvicorn main:app
```
Open `http://localhost:8000`. WebSocket-powered quiz with persistent scoreboard (SQLite).

---

## Progression

Each phase builds on the previous one:

1. **Functions → Modules** — Phase 1 teaches clean code organization
2. **Modules → Classes** — Phase 2 introduces OOP naturally through game entities
3. **Classes → Libraries** — Phase 3 shows how to use third-party packages
4. **Libraries → Algorithms** — Phase 4 dives into procedural generation and pathfinding
5. **Single-player → Multiplayer** — Phase 5 adds networking fundamentals
6. **Terminal → Web** — Phase 6 moves to async web development

---

## License

MIT
