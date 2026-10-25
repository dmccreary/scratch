# Scratch

[![MkDocs](https://img.shields.io/badge/Made%20with-MkDocs-526CFE?logo=materialformkdocs)](https://www.mkdocs.org/)
[![Material for MkDocs](https://img.shields.io/badge/Material%20for%20MkDocs-526CFE?logo=materialformkdocs)](https://squidfunk.github.io/mkdocs-material/)
[![GitHub Pages](https://img.shields.io/badge/View%20on-GitHub%20Pages-blue?logo=github)](https://dmccreary.github.io/scratch/)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-DA7857?logo=anthropic)](https://claude.ai/code)
[![Claude Skills](https://img.shields.io/badge/Uses-Claude%20Skills-DA7857?logo=anthropic)](https://github.com/dmccreary/ibook-skills)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## View the Live Site

Visit the interactive textbook at: [https://dmccreary.github.io/scratch/](https://dmccreary.github.io/scratch/)

## Overview

Resources for the interactive intelligent textbook Scratch: An Introduction to Computational Thinking

This is an interactive, AI-assisted intelligent textbook built with MkDocs and the Material theme. It is organized around a learning graph of **200 concepts** with explicit prerequisite dependencies, so that no chapter relies on a concept that has not yet been introduced. Content is organized into **13 chapters** and uses Bloom's Taxonomy (2001 revision) to target learning outcomes. The book includes **5 interactive MicroSims**.

## Site Status and Metrics

| Metric | Count |
|--------|-------|
| Concepts in Learning Graph | 200 |
| Chapters | 13 |
| MicroSims | 5 |
| Diagrams | 5 |
| Total Words | 23,577 |
| Links | 163 |
| Equivalent Pages | 98 |

**Development Stage:** Not specified

Metrics are generated from `docs/learning-graph/book-metrics.json`.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/dmccreary/scratch.git
cd scratch
```

### Install Dependencies

```bash
pip install mkdocs mkdocs-material
```

### Build and Serve Locally

```bash
mkdocs build
mkdocs serve
```

Open your browser to `http://localhost:8000`.

### Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

## Repository Structure

```
scratch/
├── docs/                          # MkDocs documentation source
│   ├── chapters/                  # Chapter content (index.md per chapter)
│   ├── sims/                      # Interactive MicroSims (main.html, script.js, index.md)
│   ├── learning-graph/            # Learning graph CSV/JSON and quality reports
│   │   ├── learning-graph.csv     # Concept dependencies
│   │   ├── learning-graph.json    # vis-network format
│   │   └── book-metrics.json      # Canonical book metrics
│   ├── glossary.md                # ISO 11179-style definitions
│   └── faq.md                     # Frequently asked questions
├── mkdocs.yml                     # MkDocs configuration
└── README.md                      # This file
```

## Reporting Issues

Found a bug, typo, or have a suggestion? Please report it at [GitHub Issues](https://github.com/dmccreary/scratch/issues).

Include a description of the problem, steps to reproduce, expected vs. actual behavior, and browser details for MicroSim problems.

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

- **Attribution** — Give appropriate credit with a link to the original
- **NonCommercial** — No commercial use without permission
- **ShareAlike** — Distribute contributions under the same license

## Acknowledgements

- **[MkDocs](https://www.mkdocs.org/)** and **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** - Static site generator and theme
- **[vis-network](https://visjs.org/)** - Learning graph visualization
- **[Claude AI](https://claude.ai)** by Anthropic - AI-assisted content generation
- **[GitHub Pages](https://pages.github.com/)** - Free hosting

## Contact

**Dan McCreary**

- LinkedIn: [linkedin.com/in/danmccreary](https://www.linkedin.com/in/danmccreary/)
- GitHub: [@dmccreary](https://github.com/dmccreary)

Questions or suggestions? Connect on LinkedIn or open an issue on [GitHub](https://github.com/dmccreary/scratch/issues).


## Additional Notes

The previous README for this repository is preserved below.

## Scratch Resources

The documentation for this site is [here](http://coderdojotc.github.io/scratch/).

This repository contains resources for the Scratch code group at CoderDojo Twin Cities.

New mentors, please check out these 6 short [Scratch Basics for New Mentors](https://github.com/CoderDojoTC/scratch/wiki/New-Scratch-Mentors-Start-Here) before you come to mentor. Experienced mentors -- we'd love your feedback and favorite tips.  Please send to hello@CoderDojoTC.org

Check out the [mentor-resource repository](https://github.com/CoderDojoTC/mentor-resources) for tips on mentoring and other useful information.

Once you are at CoderDojoTC, there are laminated [Scratch cards](http://scratch.mit.edu/help/cards/) in one of the plastic bins -- find them and make them available to the students.

### Create an Account Handouts

We've created a [handout](handouts/scratch-make-an-account.docx) to help students create and remember their account details.

Thank you for mentoring at CoderDojoTC!

All material uses the Creative Commons non-commercial attribution license:
https://creativecommons.org/licenses/by-nc/3.0/deed.en_US

We use the CoderDojo style guide here:
https://company-51033.frontify.com/d/E6KNDhunr9mR/coderdojo-style-guide-1460385526
