# GEMINI.md - Project Context & Agent Guide

## Project Overview

**Predições de Loterias da Caixa** is a project to study and experiment with mathematical and statistical models for analyzing and predicting lottery results (Mega-Sena, Lotofácil, Quina).
**Goal:** Create a "laboratory" to validate hypothesis, tracking predictions against real results with a focus on hypothetical financial performance.

## Current Status

- **Phase:** Transitioning from **Phase 1 (Foundation)** to **Phase 2 (Prediction Engine)**.
- **Environment:** DevContainer (Python).
- **Data Source:** External repository `loterias-caixa-db` (CSV files).
- **Architecture:** Object-Oriented (src/loterias), separating Data, Core Logic, and Reporting.

## Architecture

- `src/loterias/base.py`: Base classes `Lottery` and `Model`.
- `src/loterias/data_manager.py`: Handles data fetching and caching.
- `src/loterias/{game}.py`: Specific implementations (MegaSena, Lotofacil, Quina).
- `scripts/`: Analysis and execution scripts.

## Immediate Focus (Phase 2)

1. **Prediction Engine:** Create a CLI/Interface to generate predictions using different models.
2. **Initial Models:** Implement basic models (Frequency, Random, etc.) to test the pipeline.
3. **Export:** Save predictions in a structured format for later verification.

## Roadmap Summary

1. **Phase 1:** Foundation & Refactoring (✅ Complete)
2. **Phase 2:** Prediction Engine & On-Demand Service (🚧 Next)
3. **Phase 3:** Hypothetical Tracking System (Ledger & P&L)
4. **Phase 4:** Advanced Modeling (ML/AI)
5. **Phase 5:** Visualization & Static Reporting

## Key Files

- `docs/roadmap.md`: Long-term vision.
- `docs/project_plan.md`: Original plan.
- `src/loterias/`: Core source code.
