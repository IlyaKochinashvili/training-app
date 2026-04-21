# TASKS

## 0. Project setup cleanup
- [ ] Add smoke test for `/health`
- [ ] Remove unused and empty files
- [ ] Verify README and local run instructions
- [ ] Verify Makefile commands
- [ ] Verify Docker build
- [ ] Finalize clean base setup

---

## 1. PostgreSQL setup
- [ ] Replace SQLite with PostgreSQL
- [ ] Add PostgreSQL environment variables
- [ ] Update database session setup
- [ ] Verify database connection
- [ ] Add PostgreSQL container for local development
- [ ] Add database healthcheck

---

## 2. Workout session foundation
- [ ] Create workout session entity
- [ ] Add active workout session logic
- [ ] Add start workout flow
- [ ] Add finish workout flow
- [ ] Store `started_at`
- [ ] Store `finished_at`
- [ ] Add workout status

---

## 3. Exercise input parser
- [ ] Define exercise input format
- [ ] Parse first line as exercise name
- [ ] Parse set lines as `weight reps`
- [ ] Validate sets count
- [ ] Validate weight values
- [ ] Validate reps values
- [ ] Return readable validation errors

---

## 4. Exercise name normalization and filtering
- [ ] Define canonical exercise model
- [ ] Keep canonical exercise names only in Ukrainian
- [ ] Allow user input in Russian
- [ ] Normalize exercise names before matching
- [ ] Add exact match
- [ ] Add alias match
- [ ] Add fuzzy match
- [ ] Reject generic trash names
- [ ] Do not create new exercise automatically if confidence is low

---

## 5. Base exercise seed
- [ ] Create initial Ukrainian exercise list
- [ ] Add Russian aliases
- [ ] Add common typo aliases
- [ ] Add seed script or seed command
- [ ] Verify matching quality on base examples

---

## 6. Telegram bot skeleton
- [ ] Add Telegram bot base setup
- [ ] Add main menu
- [ ] Add "Почати тренування" button
- [ ] Add "Додати вправу" button
- [ ] Add "Завершити тренування" button
- [ ] Add finish confirmation flow

---

## 7. Workout flow integration
- [ ] Connect parser to active workout
- [ ] Resolve exercise before saving
- [ ] Save raw user input name separately
- [ ] Save parsed sets to active workout
- [ ] Return readable bot response after successful save

---

## 8. Tests
- [ ] Add healthcheck smoke test
- [ ] Add database connection test
- [ ] Add start workout test
- [ ] Add finish workout test
- [ ] Add exercise parser tests
- [ ] Add exercise resolver tests
- [ ] Add trash-name rejection tests