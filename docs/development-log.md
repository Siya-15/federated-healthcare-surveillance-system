## Feature: Rich Clinical Database

### Objective(s)
- Objective D
- Supports Objectives B and E

### Purpose
Extended the patient schema to capture richer clinical information required for advanced AI models and epidemiological surveillance.

### Fields Added
- district
- occupation
- severity
- symptom_duration
- recovery_days
- complications

### Future Features Enabled
- Recovery time prediction
- Complication prediction
- District-wise outbreak detection
- Personalized treatment recommendation

## Feature: Clinically Correlated Synthetic Dataset

### Objective
Objective D

### Purpose
Generate realistic patient records with meaningful relationships between disease severity, recovery time, complications, and outcomes.

### Relationships Introduced

Disease → Severity

Severity → Recovery Days

Severity → Complications

Complications → Outcome

### Future Features Enabled

Recovery prediction

Complication prediction

Personalized treatment recommendation

# Phase 2 - Recovery Time Prediction

## Objective
Objective E

## Purpose
Estimate the expected recovery duration for a patient using historical clinical records.

## Model Type
Regression

## Inputs
- Disease
- Severity
- Treatment
- Age

## Output
Recovery Days

## Status
In Progress
