# Poke-Tactician

**A Gen 1 Pokemon Battle Optimizer - CS_311 Data Structures & Algorithms Extra Credit Project**

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?logo=netlify)](https://poke-tactician-jc3p0.netlify.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61dafb?logo=react)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb)](https://www.mongodb.com/)

**Live Demo:** https://poke-tactician-jc3p0.netlify.app

---

## What is Poke-Tactician?

A full-stack web application that finds **optimal battle strategies** for Pokemon Gen 1 battles using three different algorithms:
- **Greedy** (Heap-based - Assignment 6)
- **Dynamic Programming** (Hash Table memoization - Assignment 7)
- **Dijkstra's Algorithm** (Graph shortest path - Assignments 8 & 9)

Build custom Gen 1 Pokemon teams, select a boss trainer (Champion Blue, Giovanni, or Lance), and let the optimizer calculate the best move sequence to win!

---

## Screenshots

### Home Page
![Home Page](https://raw.githubusercontent.com/JC3P0/poke-tactician/refs/heads/main/screenshots/home-page.png)

### Team Builder
Customize your Pokemon team with moves, levels, and DVs (Gen 1 individual values):

![Team Builder](https://raw.githubusercontent.com/JC3P0/poke-tactician/refs/heads/main/screenshots/team-builder.png)

### Boss Selector
Choose from legendary trainers (Blue, Giovanni, Lance):

![Boss Selector](https://raw.githubusercontent.com/JC3P0/poke-tactician/refs/heads/main/screenshots/boss-selector.png)

### Results Page
See all three algorithms compared side-by-side with detailed battle logs:

![Results Page](https://raw.githubusercontent.com/JC3P0/poke-tactician/refs/heads/main/screenshots/results-page.png)

**Real Results:** In the screenshot above, **Greedy failed** to win the battle, while **DP and Dijkstra both found victory paths**—with **Dijkstra achieving victory in 1 fewer turn!**

---

## Architecture

```
Frontend (React - Netlify)
    |
    +-> getGen1Pokemon (JS) -> MongoDB Atlas
    +-> getGen1Items (JS) -> MongoDB Atlas
    +-> battleOptimizer (Python) -> AWS Lambda
        - Greedy Algorithm (Heap - Assignment 6)
        - Dynamic Programming (Hash Table - Assignment 7)
        - Dijkstra's Algorithm (Graph - Assignments 8 & 9)
```

**Tech Stack:**
- **Frontend:** React 18, IndexedDB for team persistence
- **Backend (Netlify):** Node.js serverless functions
- **Backend (AWS Lambda):** Python 3.11 battle optimizer
- **Database:** MongoDB Atlas (151 Gen 1 Pokemon, 165+ moves)

---

## CS_311 Assignment Integration

This project integrates concepts from **CS_311 Data Structures & Algorithms** assignments:

### **Assignment 6: Heaps**
- **Greedy Algorithm** uses a max-heap to select the highest-damage move each turn
- Priority queue implementation for move selection
- Fast O(log n) extraction of best moves

### **Assignment 7: Hash Tables**
- **Dynamic Programming** uses hash table memoization to cache battle states
- O(1) lookup for previously computed optimal paths
- Stores type effectiveness lookup tables for damage calculation

### **Assignment 8 & 9: Graphs + Dijkstra's Shortest Path**
- **Battle State Graph:** Each node represents a battle state (HP, active Pokemon)
- **BFS for state exploration:** Generate all possible successor states
- **Dijkstra's Algorithm:** Finds shortest path from initial state to victory
- Optimal move sequence = shortest path through battle state graph

---

## Gen 1 Battle Mechanics

Implements authentic Pokemon Red/Blue battle mechanics:
- **DVs (0-15)** instead of modern IVs
- **Unified Special stat** (no Sp.Atk/Sp.Def split)
- **Speed-based turn order** and critical hits
- **Type effectiveness** with Gen 1 quirks (Ghost doesn't affect Psychic!)
- **Authentic Gen 1 Trainer AI** (researched from Bulbapedia/GameFAQs)

---

## How to Run Locally

### Prerequisites
- Node.js 18+
- Python 3.11+
- MongoDB connection string

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/JC3P0/poke-tactician.git
cd poke-tactician
```

**2. Install frontend dependencies:**
```bash
cd frontend
npm install
```

**3. Install Python dependencies:**
```bash
cd ../netlify/functions/battleOptimizer
pip install -r requirements.txt
```

**4. Set up environment variables:**
Create a `.env` file in the root directory:
```
MONGODB_URI=your_mongodb_connection_string
```

**5. Run the development server:**
```bash
cd frontend
npm start
```

Visit `http://localhost:3000` to use the app!

---

## Project Structure

```
poke-tactician/
├── frontend/                    # React application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── HomePage.js     # Landing page
│   │   │   ├── TeamBuilder.js  # Pokemon team customization
│   │   │   ├── BossSelector.js # Boss trainer selection
│   │   │   └── Results.js      # Algorithm comparison results
│   │   └── utils/
│   │       └── api.js          # API calls to backend
│   └── public/
├── netlify/functions/
│   ├── getGen1Pokemon.js       # Fetch Pokemon data
│   ├── getGen1Items.js         # Fetch items data
│   └── battleOptimizer/        # Python battle optimizer (deployed to AWS Lambda)
│       ├── algorithms/
│       │   ├── greedy.py       # Heap-based greedy algorithm
│       │   ├── dynamic_programming.py  # DP with hash table memoization
│       │   └── dijkstra.py     # Graph shortest path
│       ├── dataStructures/
│       │   ├── heap.py         # Max heap implementation
│       │   ├── hash_table.py   # Hash table with chaining
│       │   └── graph.py        # Graph with BFS/Dijkstra
│       ├── models/
│       │   ├── pokemon.py      # Pokemon model
│       │   ├── move.py         # Move model
│       │   └── battleState.py  # Battle state representation
│       └── utils/
│           ├── damageCalculator.py      # Gen 1 damage formula
│           └── typeEffectiveness.py     # Type matchup table
└── screenshots/                # UI screenshots
```

---

## Data Sources

- **Pokemon Data:** MongoDB Atlas with 151 Gen 1 Pokemon
- **Move Database:** 165+ Gen 1 moves with power, accuracy, type, and PP
- **Boss Trainers:** Champion Blue, Giovanni (Team Rocket), Lance (Elite Four)
- **Type Effectiveness:** Authentic Gen 1 type chart
- **Battle Mechanics:** Researched from Bulbapedia, Smogon, Pokemon Speedruns Wiki

---

## Key Features

- **Complete Gen 1 Pokedex** - All 151 Pokemon with accurate stats
- **Custom Team Builder** - Set levels, DVs, and movesets
- **3 Optimization Algorithms** - Greedy, DP, Dijkstra
- **Side-by-Side Comparison** - See which algorithm performs best
- **Detailed Battle Logs** - Turn-by-turn replay with damage tracking
- **Download Results** - Export battle data as JSON
- **Persistent Teams** - Save teams in browser (IndexedDB)
- **Authentic Gen 1 AI** - Opponent uses research-based trainer AI

---

## Example Battle Output

```json
{
  "algorithm": "dijkstra",
  "result": "victory",
  "turns": 16,
  "totalDamage": 3842,
  "moveSequence": [
    {"turn": 1, "pokemon": "Charizard", "move": "Fire Blast", "damage": 198},
    {"turn": 2, "pokemon": "Charizard", "move": "Fire Blast", "damage": 204}
  ],
  "battleLog": [
    {
      "turn": 1,
      "event": "player_attack",
      "attacker": {"name": "Charizard", "hp": 266, "maxHp": 266},
      "defender": {"name": "Gyarados", "hpBefore": 290, "hpAfter": 92, "maxHp": 290},
      "move": "Fire Blast",
      "damage": 198,
      "effectiveness": 2.0
    }
  ]
}
```

---

## Academic Report

This project includes a comprehensive academic report analyzing:
- **Algorithm implementation** (Greedy, DP, Dijkstra)
- **Data structure usage** (Heap, Hash Table, Graph)
- **Performance comparison** and complexity analysis
- **Gen 1 battle mechanics** with proper citations
- **Results and conclusions**

---

## License

MIT License - See [LICENSE](LICENSE) for details.

**Note:** Pokemon and all related properties are © Nintendo, Game Freak, and The Pokémon Company. This is a fan-made educational project not affiliated with or endorsed by The Pokémon Company.

---

## Author

**Joshua Clemens**
CS_311 Data Structures & Algorithms
Extra Credit Project
Fall 2025

---

## Acknowledgments

- **Bulbapedia** - Gen 1 mechanics documentation
- **Pokemon Speedruns Wiki** - Trainer AI algorithms
- **Smogon University** - Competitive Pokemon resources
- **PokéAPI** - Pokemon data

---

*"Finding the optimal path... one battle at a time!"*

---

**Last Updated:** December 9, 2025
**Live Demo:** https://poke-tactician-jc3p0.netlify.app
