## Functional Requirements

1. User Registration – The system shall allow users to register by providing a username, email, and password.           DONE
2. User Login – The system shall authenticate users based on their credentials to allow access.                         DONE
3. User Logout – The system shall allow logged-in users to securely log out.                                            DONE
4. Create Recipe – The system shall allow users to create and submit new recipes with ingredients and instructions.     DONE
5. Edit Recipe – The system shall allow users to edit their own submitted recipes.
6. Delete Recipe – The system shall allow users to delete their own submitted recipes.                                  DONE
7. View Recipe – The system shall allow all users to view any published recipe.                                         DONE
8. Search Recipe – The system shall allow users to search for recipes by keywords.
9. Rate Recipe – The system shall allow users to rate recipes on a scale (e.g., 1–5 stars).                             DONE
10. Comment on Recipe – The system shall allow users to leave comments on recipe pages.                                 DONE
11. View User Profile – The system shall allow users to view their own profile including submitted recipes.
12. Edit User Profile – The system shall allow users to edit their display name, email, or password.
13. Save Recipe (Favorites) – The system shall allow users to save recipes to their favorites list.                     DONE
14. View All Recipes – The system shall allow users to view a list of all publicly available recipes.                   DONE
15. Filter Recipes – The system shall allow users to filter recipes by tags such as 'vegan', 'dessert', etc.

## Non-functional Requirements
1. The system shall load recipe pages in under 2 seconds
2. The system should support more than 100 users without performance issues

## Use Cases

1. User Registration (Written and will be implemented by Eric)
- **Pre-condition:** Visitor is not logged in and has a valid email address.
- **Trigger:** Visitor clicks “Sign Up” on the website.
- **Primary Sequence:**
1. Visitor accesses the registration page and fills in username, email, and password.
2. Visitor submits the registration form.
3. System validates the data and creates a new user account.
4. System logs the user in or redirects them to the login page.
- **Primary Postconditions:** A new user account is created and stored in the system.
- **Alternate Sequence:**
1. Email already exists: System notifies user and suggests logging in.
2. Weak password: System asks for a stronger password.
3. Missing fields: System prompts user to complete all required inputs.
4. Server error: System shows failure message and retry option.

2. User Login (Written and will be implemented by Eric)
- **Pre-condition:** User has an existing account with valid email and password.
- **Trigger:** User clicks the “Login” button from the homepage or any restricted page.
- **Primary Sequence:**
1. User enters their email and password on the login form.
2. User submits the form.
3. System verifies the credentials.
4. If valid, system logs the user in and redirects to the dashboard.
- **Primary Postconditions:** User is authenticated and has access to protected features.
- **Alternate Sequence:**
1. Invalid email or password: System displays an error message.
2. Empty fields: System prompts user to fill in required inputs.
3. Account inactive: System informs user and provides help link.
4. Technical issue: System suggests retrying later.

3. User Logout (Written and will be implemented by Eric)
- **Pre-condition:** User is currently logged in.
- **Trigger:** User clicks the “Logout” button from the navigation bar or menu.
- **Primary Sequence:**
1. User clicks the logout action.
2. System processes the logout request.
3. System destroys the user session.
4. System redirects user to the homepage or login screen.
- **Primary Postconditions:** User is logged out and no longer has access to protected resources.
- **Alternate Sequence:**
1. Session already expired: User is redirected to the login page.
2. Logout fails: System displays an error message and retry option.

4. Create Recipe (Written and will be implemented by Eric)
- **Pre-condition:** User must be logged in.
- **Trigger:** User clicks the “Create Recipe” button or menu item.
- **Primary Sequence:**
1. User accesses the create recipe form.
2. User fills in title, description, ingredients, and instructions.
3. User submits the form.
4. System saves the recipe and redirects to the recipe detail page.
- **Primary Postconditions:** A new recipe is stored and visible under the user’s account.
- **Alternate Sequence:**
1. Missing fields: System prompts user to complete the form.
2. Invalid input: System highlights errors.
3. Session expired: User is redirected to login page.
4. System error: Recipe not saved, and user is asked to retry.

5. Edit Recipe (Written and will be implemented by Eric)
- **Pre-condition:** User is logged in and owns the recipe they want to edit.
- **Trigger:** User clicks the “Edit” button on one of their recipes.
- **Primary Sequence:**
1. User views their recipe and clicks “Edit.”
2. System shows a form pre-filled with the recipe’s details.
3. User updates fields and submits the form.
4. System validates and saves the changes, then redirects to updated recipe.
- **Primary Postconditions:** The recipe is updated in the system with the new details.
- **Alternate Sequence:**
1. User tries to edit a recipe they don’t own: Access is denied.
2. Invalid input: System highlights errors for correction.
3. Recipe deleted before submission: System shows error.
4. System issue: Changes not saved, and user is notified.

# 6. Delete Recipe (Written and will be implemented by Rustico)
- **Pre-condition:**
User is logged into the webpage.
- **Trigger:**
User presses delete button on a recipe that they own (created).
- **Primary Sequence:**
1. User presses delete button on a recipe.
2. Prompt opens to confirm the user wants to delete the recipe.
3. The recipe chosen is removed from the database.
4. User is informed that the recipe has been successfully deleted.
5. Page is refreshed after user acknowledges the information.
- **Primary Postconditions:** 
Recipe has been deleted from the database and is no longer stored.
- **Alternate Sequence:**
1. User presses delete button on a recipe.
2. Prompt opens to confirm the user wants to delete the recipe.
3. Recipe cannot be found when searching the database to delete it.
4. User is informed that the chosen recipe already doesn't exist.
5. Page is refreshed after user acknowledges the information.

# 7. View Recipe (Written and will be implemented by Rustico)
- **Pre-condition:**
User is logged into the webpage.
- **Trigger:**
User presses delete button on a recipe that they own (created).
- **Primary Sequence:**
1. User uses some recipe access (search bar, direct URL, filter, etc).
2. Prompt opens to confirm the user wants to delete the recipe.
3. The recipe chosen is removed from the database.
4. User is informed that the recipe has been successfully deleted.
- **Primary Postconditions:** 
Recipe has been deleted from the database and is no longer stored.
- **Alternate Sequence:**
1. User presses delete button.
2. Prompt opens to confirm the user wants to delete the recipe.
3. Recipe cannot be found when searching the database to delete it.
4. User is informed that the chosen recipe already doesn't exist.

# 8. Search Recipe (Written and will be implemented by Rustico)
1. User types in a search parameter (tag, name, etc.) into search bar.
2. A page listing all relevant recipes is shown.
3. User looks for the specific recipe they are interested in (scrolling through the list).
4. The user finds their desired recipe and clicks a link to access the recipe's page.
- **Primary Postconditions:**
N/A - No data was added or changed (considering current use cases and functionality).
- **Alternate Sequence:**
1. User types in a search parameter (tag, name, etc.) into search bar.
2. No recipes are found with the specificied keywords and search parameters.
3. User is informed that no results have been found.

# 9. Rate Recipe (Written and will be implemented by Rustico)
- **Pre-condition:**
User has an account in the database.
User is logged into the webpage.
The recipe to rate exists in the database.
- **Trigger:**
User presses rate button on a recipe that they do not own (created).
1. User types in a search parameter (tag, name, etc.) into search bar.
2. A page listing all relevant recipes is shown.
3. User looks for the specific recipe they are interested in (scrolling through the list).
4. The user finds their desired recipe and clicks a link to access the recipe's page.
- **Primary Postconditions:**
Average rating of a rated recipe is updated and stored.
- **Alternate Sequence:**
1. User uses some recipe access (search bar, direct URL, filter, account, etc).
2. User presses rate button on their own created recipe and rates the recipe out of 5 stars.
3. User is informed that they cannot rate their own recipes.

# 10. Comment on Recipe (Written and will be implemented by Rustico)
- **Pre-condition:**
User has an account in the database.
User is logged into the webpage.
The recipe to comment on exists in the database.
- **Trigger:**
User presses comment button on a recipe regardless of ownership.
1. User uses some recipe access (search bar, direct URL, filter, account, etc).
2. User presses comment button on the page of the specific recipe they'd like to comment on.
3. A text box appears and the user types out their comment.
4. User presses submit and the comment is appended to the recipe.
- **Primary Postconditions:**
Information about comment count and accessible comments updates accordingly (comment shows on recipe, number increases by one).
- **Alternate Sequence:**
1. User uses some recipe access (search bar, direct URL, filter, account, etc).
2. User presses comment button on the page of the specific recipe they'd like to comment on.
3. A text box appears and the user types out their comment.
4. User presses submit, but the recipe no longer exists (deleted by recipe owner or admin while the user was commenting).
5. User is informed that the recipe no longer exists and cannot be commented on.

11. Edit User Profile (Written and will be implemented by Jesse)
- **Pre-condition:** 
- User must have an existing account
- User must be logged in
- **Trigger:** User selects edit my profile which asks them to update their display name, email, or password.
- **Primary Sequence:**
1. User opens up website
2. User navigates to button that says edit my profile
3. User enters name, email, and password they wish to update to
- **Primary Postconditions:** User’s display name, email, and password are successfully updated
- **Alternate Sequence:**
1. Database unable to retrieve user profile
2. User is not logged in in order to edit profile

12. Save Recipe (Favorites) (Written and will be implemented by Jesse)
- **Pre-condition:** 
- User must have an existing account
- User must be logged in
- **Trigger:** User clicks on favorite recipe from the / endpoint
- **Primary Sequence:**
1. User opens up website by going to / endpoint
2. User clicks on favorite on the recipe they want to save
3. System verifies if user is logged in
4. System saves the recipes favorites to data base
- **Primary Postconditions:** Favorite recipes are successfully saved for the user
- **Alternate Sequence:**
1. User is not logged in
2. Database save error

13. View All Recipes (Written and will be implemented by Jesse)
- **Pre-condition:** There must be a minimum of 1 recipe to view in order to view all recipes
- **Trigger:** User navigated to / endpoint to view all recipes
- **Primary Sequence:**
1. User navigates to website to the / endpoint
2. System queries the database to retrieve all recipes 
3. System displays all recipes  to the user
- **Primary Postconditions:** All recipes are successfully displayed 
- **Alternate Sequence:**
1. Database fails to retrieve all recipes
2. No recipes written to database when visiting / endpoint 

14. Filter Recipes (Written and will be implemented by Jesse)
- **Pre-condition:** User must be on the recipe browsing page
- **Trigger:** User selects a filter or tag
- **Primary Sequence:**
1. User navigates to browsing section of website
2. User clicks or selects the tag
3. System will query recipes containing that specific tag
- **Primary Postconditions:** Filtered recipes are successfully displayed
- **Alternate Sequence:**
1. System does not find any recipe with the matching filter

15. View User Profile (Written and will be implemented by Jesse)
- **Pre-condition:** 
- User must have an existing account  
- User must be logged in  
- **Trigger:** User selects view profile and recipes of user are displayed  
- **Primary Sequence:**
1. User opens up website
2. User navigates to profile he/she wants to view 
3. User selects view profile
4. System retrieves profile from database
5. System displays recipes created by user
- **Primary Postconditions:** User profile along with recipes are successfully displayed as output
- **Alternate Sequence:**
1. No wifi connection
2. No profile to view. Profile unavailable
