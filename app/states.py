# import reflex as rx
# import httpx

# class LoginState(rx.State):
#     username: str = ""
#     password: str = ""
#     login_error: str = ""
#     is_logged_in: bool = False
#     user_id: str = ""
    
#     async def handle_login(self):
#         try:
#             if not self.username or not self.password:
#                 self.login_error = "Please enter both username and password"
#                 return

#             async with httpx.AsyncClient() as client:
#                 response = await client.post(
#                     "http://localhost:8000/login",
#                     json={"username": self.username, "password": self.password}
#                 )

#                 if response.status_code == 200:
#                     result = response.json()
                    
#                     # Update state
#                     self.login_error = ""
#                     self.is_logged_in = True
#                     self.user_id = result.get("user_id", "")
                    
#                     # Use yield instead of return for Reflex state updates
#                     yield rx.window_alert("Login successful!")
#                     yield rx.redirect("/main")  # Redirect properly
#                 else:
#                     # Handle login error
#                     result = response.json()
#                     self.login_error = result.get("detail", "Invalid username or password")

#         except Exception as e:
#             self.login_error = f"An error occurred: {str(e)}"

    
#     def check_login(self):
#         """Verify login status when components initialize."""
#         return self.is_logged_in
    
#     def logout(self):
#         """Handle user logout."""
#         self.is_logged_in = False
#         self.username = ""
#         self.password = ""
#         self.user_id = ""
#         return rx.redirect("/")
    
# class SignupState(rx.State):
#     username: str = ""
#     password: str = ""
#     email: str = ""
#     signup_error: str = ""
#     is_signed_up: bool = False
#     user_id: str = ""

#     async def handle_signup(self):
#         try:
#             if not self.username or not self.password or not self.email:
#                 self.signup_error = "Please fill in all fields"
#                 return

#             async with httpx.AsyncClient() as client:
#                 response = await client.post(
#                     "http://localhost:8000/signup",
#                     json={"username": self.username, "password": self.password, "email": self.email}
#                 )

#                 if response.status_code == 200:
#                     result = response.json()

#                     # Update both SignupState and LoginState
#                     self.signup_error = ""
#                     self.is_signed_up = True

#                     # Automatically log in the user after successful signup
#                     LoginState.is_logged_in = True
#                     LoginState.user_id = result.get("user_id", "")
#                     LoginState.username = self.username  # Optional

#                     yield rx.window_alert("Signup successful!")
#                     yield rx.redirect("/main")  # Redirect properly
#                 else:
#                     result = response.json()
#                     self.signup_error = result.get("detail", "Signup failed")

#         except Exception as e:
#             self.signup_error = f"An error occurred: {str(e)}"    




import reflex as rx



class Main_Pages_state(rx.State):
    """The app state."""

    # Add search text state
    search_text: str = ""
    display_text: str = ""  # Store the displayed text
    filtered_mindmaps: list[dict] = []  # New state var for filtered results#!!!!!
    filtered_contests: list[dict] = []  # New state var for filtered contests#!!!!!


    def set_search(self, value: str):
        """Set the search text."""
        self.search_text = value

    # @rx.event
    # def handle_search(self):
    #     """Handle search button click."""
    #     self.display_text = self.search_text
    #     return rx.redirect(f"/search?q={self.search_text}")
    @rx.event
    def handle_search(self):
        """Handle search button click for main page"""
        if not self.search_text:
            return
        self.display_text = self.search_text
        
        # Split into individual words and filter out empty strings
        search_words = [word.lower() for word in self.search_text.split() if word]
        
        # Filter mindmaps - match if any search word is in the name
        self.filtered_mindmaps = [
            mindmap for mindmap in self.Mind_map
            if any(word in mindmap["name"].lower() for word in search_words)
        ]

        # Filter contests - match if any search word is in the name
        self.filtered_contests = [
            contest for contest in self.Contest
            if any(word in contest["name"].lower() for word in search_words)
        ]

        return rx.redirect("/search")

    @rx.event 
    def handle_search_page(self):
        """Handle search button click for search page"""
        if not self.search_text:
            return
        self.display_text = self.search_text

        # Split into individual words and filter out empty strings
        search_words = [word.lower() for word in self.search_text.split() if word]
        
        # Filter mindmaps - match if any search word is in the name
        self.filtered_mindmaps = [
            mindmap for mindmap in self.Mind_map
            if any(word in mindmap["name"].lower() for word in search_words)
        ]

        # Filter contests - match if any search word is in the name
        self.filtered_contests = [
            contest for contest in self.Contest
            if any(word in contest["name"].lower() for word in search_words)
        ]



    @rx.var
    def check_results(self) -> str:
        # Both empty
        if len(self.filtered_mindmaps) == 0 and len(self.filtered_contests) == 0:
            return "none"
        # Only mindmaps have results
        elif len(self.filtered_mindmaps) > 0 and len(self.filtered_contests) == 0:
            return "mindmaps_only"
        # Only contests have results  
        elif len(self.filtered_mindmaps) == 0 and len(self.filtered_contests) > 0:
            return "contests_only"
        # Both have results
        else:
            return "both"

    # User data

    current_user: dict[str, str] = {
        "username": "Bewieee",  # Default user name
        "email": "66011148@kmitl.ac.th",
        "password": "12345678",
        "bookmark_mindmap" : [],
        "achievements_ids": [],
        "user_id": "1234567890",
        "avatar": "/prettestGirlInDaWorldo.png"
    }


    # Recent mindmaps data
    recent_mindmaps: list[dict] = [
        {
            "name": "Chinese Sentences",
            "terms": 27,
            "creator": "Sarita",
            "image": "/mindmaptail.png"
        },
        {
            "name": "German Sentences", 
            "terms": 27,
            "creator": "Sarita",
            "image": "/mindmaptail.png"
        },
        {
            "name": "Python Programming",
            "terms": 109, 
            "creator": "Sarita",
            "image": "/mindmaptail.png"
        },
        {
            "name": "I Love AI",
            "terms": 12,
            "creator": "Sarita", 
            "image": "/mindmaptail.png"
        }
    ]

    # Favorite mindmaps data 
    favorite_mindmaps: list[dict] = [
        {
            "name": "Python is the Best",
            "terms": 27,
            "creator": "Prang",
            "avatar": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "terms": 12, 
            "creator": "Khaopun",
            "avatar": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "terms": 20,
            "creator": "Bew",
            "avatar": "/static/logo.png" 
        }
    ]

    # Top creators data
    top_creators: list[dict] = [
        {
            "name": "Prang",
            "mindmap_count": 12,
            "contest_count": 5,
            "avatar": "/static/logo.png"
        },
        {
            "name": "karina",
            "mindmap_count": 5,
            "contest_count": 2,
            "avatar": "/static/logo.png"
        },
        {
            "name": "AsaBm",
            "mindmap_count": 122,
            "contest_count": 52,
            "avatar": "/static/logo.png"
        }
    ]

    # all mindmaps data 
    Mind_map: list[dict] = [
        {
            "name": "Python is the Best",
            "terms": 27,
            "creator": "Prang",
            "avatar": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "terms": 12, 
            "creator": "Khaopun",
            "avatar": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "terms": 20,
            "creator": "Bew",
            "avatar": "/static/logo.png" 
        }
    ]

    # all contests data 
    Contest: list[dict] = [
        {
            "name": "Python is the Best",
            "sets": 27,
            "creator": "Prang",
            "avatar": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "sets": 12, 
            "creator": "Khaopun",
            "avatar": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "sets": 20,
            "creator": "Bew",
            "avatar": "/static/logo.png" 
        },
        {
            "name": "C++ for u",
            "sets": 5,
            "creator": "bbeee",
            "avatar": "/static/logo.png" 
        }
    ]
