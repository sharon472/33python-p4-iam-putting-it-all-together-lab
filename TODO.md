# IAM Lab Implementation TODO

## Phase 1: Clean up and fix app.py

- [ ] Remove duplicate Flask app setup code
- [ ] Convert function-based routes to Flask-RESTful Resources
- [ ] Register all resources with the API

## Phase 2: Implement Flask-RESTful Resources

- [ ] Signup Resource (POST /signup)
- [ ] CheckSession Resource (GET /check_session)
- [ ] Login Resource (POST /login)
- [ ] Logout Resource (DELETE /logout)
- [ ] RecipeIndex Resource (GET /recipes, POST /recipes)

## Phase 3: Testing

- [ ] Run model tests: pytest testing/models_testing/
- [ ] Run app tests: pytest testing/app_testing/
- [ ] Run full test suite: pytest

## Phase 4: Verification

- [ ] Verify database migrations
- [ ] Test with seed data
- [ ] Verify all requirements are met
