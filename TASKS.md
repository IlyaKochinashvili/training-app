# TASKS

## 0. Project setup cleanup
- [x] Add smoke test for `/health`
- [x] Remove unused and empty files
- [x] Verify README and local run instructions
- [x] Verify Makefile commands
- [ ] Verify Docker build
- [x] Finalize clean base setup

---

## 1. PostgreSQL setup
- [x] Replace SQLite with PostgreSQL
- [x] Add PostgreSQL environment variables
- [x] Update database session setup
- [ ] Verify database connection
- [x] Add PostgreSQL container for local development
- [x] Add database healthcheck

---

## 2. Workout session foundation
- [x] Create workout session entity
- [x] Add active workout session logic
- [x] Add start workout flow
- [x] Add finish workout flow
- [x] Store `started_at`
- [x] Store `finished_at`
- [x] Add workout status

---

## 3. Exercise input parser
- [x] Define exercise input format
- [x] Parse first line as exercise name
- [x] Parse set lines as `weight reps`
- [x] Validate sets count
- [x] Validate weight values
- [x] Validate reps values
- [x] Return readable validation errors

---

## 4. Exercise name normalization and filtering
- [x] Define canonical exercise model
- [x] Keep canonical exercise names only in Ukrainian
- [x] Allow user input in English
- [x] Normalize exercise names before matching
- [x] Add exact match
- [x] Add alias match
- [x] Add fuzzy match
- [x] Reject generic trash names
- [x] Do not create new exercise automatically if confidence is low

---

## 5. Base exercise seed
- [x] Create initial Ukrainian exercise list
- [x] Add English aliases
- [x] Add common typo aliases
- [x] Add seed script or seed command
- [ ] Verify matching quality on base examples

---

## 6. Telegram bot skeleton
- [x] Add Telegram bot base setup
- [x] Add main menu
- [x] Add "Почати тренування" button
- [x] Add "Додати вправу" (через текстовий ввід)
- [x] Add "Завершити тренування" button
- [x] Add finish confirmation flow

---

## 7. Workout flow integration
- [x] Connect parser to active workout
- [x] Resolve exercise before saving
- [x] Save raw user input name separately
- [x] Save parsed sets to active workout
- [x] Return readable bot response after successful save

---

## 8. Tests
- [x] Add healthcheck smoke test
- [ ] Add database connection test
- [ ] Add start workout test
- [ ] Add finish workout test
- [x] Add exercise parser tests
- [x] Add exercise resolver tests
- [x] Add trash-name rejection tests

---

## 9. User profile onboarding
- [ ] Create user profile model (height, weight, age, sex)
- [ ] Add user profile migration
- [ ] Add onboarding flow on first `/start`
- [ ] Ask height → weight → age → sex step by step
- [ ] Save profile to DB
- [ ] Allow user to update profile via `/profile`
- [ ] Use profile data in progression calculations

---

## 10. Workout input UX
- [ ] Show format hint before user enters exercise
- [ ] Format hint in Ukrainian with example
- [ ] Accept input as multiline: name on first line, then `weight reps` per line
- [ ] On format error — show hint again with specific error
- [ ] Support decimal weight with dot and comma (e.g. `102.5` or `102,5`)
- [ ] Add `/cancel` command to exit current state
- [ ] Show set summary after saving (weight × reps per set)

---

## 11. Progression algorithm
- [ ] Define double progression model (reps first, then weight)
- [ ] Calculate 1RM estimate from set data (Epley formula)
- [ ] Store per-exercise history per user
- [ ] After workout — show next session recommendations per exercise
- [ ] Recommendation: target weight + rep range based on RIR history
- [ ] Show trend: improving / maintaining / regressing
