<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:16a34a&height=180&section=header&text=PERT%20Estimator&fontColor=ffffff&fontSize=38" alt="PERT Estimator banner"/>
  <br/><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=2600&pause=700&center=true&vCenter=true&width=650&lines=Estimate+with+three-point+durations;Resolve+task+dependencies;Find+the+longest+project+path" alt="Animated title"/>
  <br/><img src="https://img.shields.io/github/license/CyberLoop-dev/pert-estimator" alt="License"/> <img src="https://img.shields.io/github/languages/top/CyberLoop-dev/pert-estimator" alt="Language"/> <img src="https://img.shields.io/github/stars/CyberLoop-dev/pert-estimator" alt="Stars"/> <img src="https://img.shields.io/github/last-commit/CyberLoop-dev/pert-estimator" alt="Last commit"/>
  <br/><img src="assets/mark.svg" width="210" alt="PERT critical path illustration"/>
</p>

## 🧭 Overview

PERT Estimator is a dependency-free Python CLI for three-point task estimates. It calculates expected durations, earliest start/finish times, and one longest dependency path.

## ✨ Features

- 📐 Calculate expected duration with `(optimistic + 4 × likely + pessimistic) / 6`.
- 🔗 Respect task dependencies and topologically order the plan.
- 🧭 Identify one critical path and its approximate variance.
- 🚧 Detect duplicate IDs, unknown dependencies, and dependency cycles.
- 📄 Print a readable table or machine-friendly JSON.

## 🎬 Demo

The included task graph contains parallel and dependent work. Run it to see expected durations and the longest path. No hosted demo is claimed.

## 🚀 Quick Start

Requires Python 3.10 or newer.

```bash
python main.py sample/tasks.json
```

For JSON output:

```bash
python main.py sample/tasks.json --json
```

## 🧰 Tech Stack

- 🐍 Python 3.10+
- 📚 Standard library only
- 📦 No third-party dependencies

## 🗂️ Folder Structure

```text
pert-estimator/
├── assets/mark.svg
├── main.py
├── sample/tasks.json
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## 🛣️ Roadmap

- [ ] Report multiple equally long critical paths.
- [ ] Export a Mermaid dependency diagram.
- [ ] Add CSV task input.

## 🤝 Contributing

Add small sample graphs for parallel work, cycles, and missing dependencies. Keep calculations deterministic and document assumptions.

## 📄 License

MIT licensed. See [LICENSE](LICENSE).

<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:16a34a,100:111827&height=105&section=footer" alt="Wave footer"/></p>
