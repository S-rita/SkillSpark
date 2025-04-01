import reflex as rx
from typing import List, Optional
import httpx
from datetime import date, datetime

class LoginState(rx.State):
    username: str = ""
    password: str = ""
    login_error: str = ""
    is_logged_in: bool = False
    user_id: str = ""
    
    async def handle_login(self):
        try:
            if not self.username or not self.password:
                self.login_error = "Please enter both username and password"
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/login",
                    json={"username": self.username, "password": self.password}
                )

                if response.status_code == 200:
                    result = response.json()
                    self.login_error = ""
                    self.is_logged_in = True
                    self.user_id = result.get("user_id", "")
                    yield rx.window_alert("Login successful!")
                    yield rx.redirect("/main")
                else:
                    result = response.json()
                    self.login_error = result.get("detail", "Invalid username or password")
        except Exception as e:
            self.login_error = f"An error occurred: {str(e)}"

    def logout(self):
        self.is_logged_in = False
        self.username = ""
        self.password = ""
        self.user_id = ""
        return rx.redirect("/")

class SignupState(rx.State):
    username: str = ""
    password: str = ""
    email: str = ""
    signup_error: str = ""
    is_signed_up: bool = False
    user_id: str = ""

    async def handle_signup(self):
        try:
            if not self.username or not self.password or not self.email:
                self.signup_error = "Please fill in all fields"
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/signup",
                    json={
                        "username": self.username,
                        "password": self.password,
                        "email": self.email,
                    },
                )

                if response.status_code == 200:
                    result = response.json()
                    self.signup_error = ""
                    self.is_signed_up = True
                    self.user_id = result.get("user_id", "")

                    yield rx.window_alert("Signup successful!")
                    yield rx.redirect("/main")
                else:
                    result = response.json()
                    self.signup_error = result.get("detail", "Signup failed")
        except Exception as e:
            self.signup_error = f"An error occurred: {str(e)}"

class CreateContestState(rx.State):
    # UI-related
    show_mindmap_list: bool = False
    selected_mindmaps: list[dict] = []

    # End date (final date)
    due_day: str = ""
    due_month: str = ""
    due_year: str = ""

    # Start date
    start_day: str = ""
    start_month: str = ""
    start_year: str = ""

    # Contest info
    contest_name: str = ""
    description: str = ""

    # Feedback
    error_message: str = ""
    success_message: str = ""
        
    folders: List[dict] = []

    month_options: dict = {
        "January": "1",
        "February": "2", 
        "March": "3",
        "April": "4",
        "May": "5",
        "June": "6",
        "July": "7",
        "August": "8",
        "September": "9",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    # Static mock list
    available_mindmaps: list[dict] = [
        {"mindmap_id": "11", "name": "History of AI", "creator_id": "1", "accessibility": True, "terms": 12},
        {"mindmap_id": "22", "name": "Intro to Philosophy", "creator_id": "2", "accessibility": False, "terms": 8},
        {"mindmap_id": "33", "name": "UI Design Patterns", "creator_id": "3", "accessibility": True, "terms": 10},
        {"mindmap_id": "44", "name": "Python Basics", "creator_id": "4", "accessibility": False, "terms": 14},
    ]

    # Toggle list
    def toggle_mindmap_list(self):
        self.show_mindmap_list = not self.show_mindmap_list

    def toggle_mindmap_selection_by_id(self, mindmap_id: str):
        mindmap = next((m for m in self.available_mindmaps if m["mindmap_id"] == mindmap_id), None)
        if not mindmap:
            return
        if mindmap in self.selected_mindmaps:
            self.selected_mindmaps.remove(mindmap)
        else:
            self.selected_mindmaps.append(mindmap)

    def is_selected(self, mindmap: dict) -> bool:
        return any(m["mindmap_id"] == mindmap["mindmap_id"] for m in self.selected_mindmaps)
    
    # Setters
    def set_contest_name(self, value: str):
        self.contest_name = value

    def set_description(self, value: str):
        self.description = value

    def set_start_day(self, value: str):
        self.start_day = value

    @rx.var
    def month_numbers_to_names(self) -> dict:
        return {v: k for k, v in self.month_options.items()}

    @rx.var
    def month_names(self) -> List[str]:
        return list(self.month_options.keys())

    @rx.var
    def display_month(self) -> str:
        """Convert the stored number back to month name for display."""
        if not self.start_month:
            return ""
        return self.month_numbers_to_names.get(self.start_month, "")

    def set_start_month(self, month_name: str):
        """Convert month name to number and store it."""
        self.start_month = self.month_options[month_name]

    def set_start_year(self, value: str):
        self.start_year = value

    @rx.var
    def display_due_month(self) -> str:
        """Convert the stored number back to month name for display."""
        if not self.due_month:
            return ""
        return self.month_numbers_to_names.get(self.due_month, "")
        
    def set_due_month(self, month_name: str):
        """Convert month name to number and store it."""
        self.due_month = self.month_options[month_name]
        
    def set_due_year(self, value: str):
        self.due_year = value

    def reset_input(self):
        self.contest_name = ""
        self.description = ""
        self.start_day = ""
        self.start_month = ""
        self.start_year = ""
        self.due_day = ""
        self.due_month = ""
        self.due_year = ""
        self.show_mindmap_list = False
        self.selected_mindmaps = []
        self.error_message = ""
        self.success_message = ""

    # Create contest
    async def create_contest(self, creator_id: str):
        try:
            if not all([
                self.contest_name,
                self.description,
                self.start_day, self.start_month, self.start_year,
                self.due_day, self.due_month, self.due_year,
            ]):
                self.error_message = "Please fill in all required fields"
                mindmap_ids = [m["mindmap_id"] for m in self.selected_mindmaps]
                print(mindmap_ids)
                return

            # Format dates
            start_date = f"{self.start_year.zfill(4)}-{self.start_month.zfill(2)}-{self.start_day.zfill(2)}"
            final_date = f"{self.due_year.zfill(4)}-{self.due_month.zfill(2)}-{self.due_day.zfill(2)}"
            created_date = date.today().isoformat()

            # Extract mindmap IDs
            mindmap_ids = [m["mindmap_id"] for m in self.selected_mindmaps]

            payload = {
                "contest_name": self.contest_name,
                "creator_id": creator_id,
                "created_date": created_date,
                "start_date": start_date,
                "final_date": final_date,
                "mindmap_ids": mindmap_ids,
                "participant_ids": [],
                "description": self.description,
            }

            print("🔹 Sending payload:", payload)

            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/contests/", json=payload)

                print("🔸 Response:", response.status_code, response.text)

                if response.status_code == 200:
                    self.success_message = "Contest created successfully!"
                    self.error_message = ""
                    yield rx.window_alert("Contest created!")
                    yield rx.redirect("/main")
                else:
                    try:
                        result = response.json()
                        self.error_message = result.get("detail", "Failed to create contest")
                    except Exception:
                        self.error_message = f"Server error ({response.status_code}): {response.text}"

        except Exception as e:
            self.error_message = f"An error occurred: {str(e)}"

# ---- Library State ----
class Library(rx.State):
    user_id: str = "user123"  
    active_tab: str = "mindmaps"  
    sort_option: str = "name_asc"  
    search_query: str = ""
    sort_refresh: bool = False

    all_mindmaps: List[dict] = []
    contests: List[dict] = []
    folders: List[dict] = []
    favourites: List[dict] = []

    error_message: str = ""
    
    # for Bookmark Mindmaps
    mock_user_data = [
        {"user_id": "user123","username": "Aroj", "email": "aroj@gmail.com", "password": "12345","bookmark_mindmap": ["m1","m2", "m3"],"achievement_ids": ["a1","a2"]},
    ]
    
    # for owned Mindmaps
    mock_mindmaps_data = [
        {"mindmap_id": "m1", "mindmap_name": "Python Basics", "created_date": "2024-01-10", "creator_id": "user123", "accessibility": True, "terms": 10},
        {"mindmap_id": "m2", "mindmap_name": "Data Structures", "created_date": "2024-02-05", "creator_id": "user123", "accessibility": True, "terms": 20},
        {"mindmap_id": "m3", "mindmap_name": "React Concepts", "created_date": "2024-03-15", "creator_id": "user456", "accessibility": True, "terms": 40},
        {"mindmap_id": "m4", "mindmap_name": "randon", "created_date": "2024-03-12", "creator_id": "user123", "accessibility": True, "terms": 30},
        {"mindmap_id": "m5", "mindmap_name": "Rhahahahaha", "created_date": "2024-04-15", "creator_id": "user123", "accessibility": True, "terms": 60},
        {"mindmap_id": "m4", "mindmap_name": "randon", "created_date": "2024-03-12", "creator_id": "user123", "accessibility": True, "terms": 30},
        {"mindmap_id": "m5", "mindmap_name": "Rhahahahaha", "created_date": "2024-04-15", "creator_id": "user123", "accessibility": True, "terms": 60},
        {"mindmap_id": "m4", "mindmap_name": "randon", "created_date": "2024-03-12", "creator_id": "user123", "accessibility": True, "terms": 30},
        {"mindmap_id": "m5", "mindmap_name": "Rhahahahaha", "created_date": "2024-04-15", "creator_id": "user123", "accessibility": True, "terms": 60},
    ]
    
    # for owned Contests 
    mock_contests_data = [
        {"contest_name": "A", "created_date": "2024-01-10", "creator_id": "user123", "start_date": "2024-01-15", "final_date": "2024-02-15", "mindmap_ids": ["m1"], "participant_ids": ["p1","p2"], "description": "Learn the basics of Python programming."},
        {"contest_name": "B", "created_date": "2024-02-05", "creator_id": "user123" , "start_date": "2024-02-10", "final_date": "2024-03-10", "mindmap_ids": ["m2"], "participant_ids": ["p1","p2"], "description": "Understand various data structures."},
        {"contest_name": "C", "created_date": "2024-03-15", "creator_id": "user456" , "start_date": "2024-03-20", "final_date": "2024-04-20", "mindmap_ids": ["m3"], "participant_ids": [], "description": "Explore React concepts."},
        {"contest_name": "D", "created_date": "2024-03-12", "creator_id": "user123", "start_date": "2024-03-15", "final_date": "2024-04-15", "mindmap_ids": ["m4"], "participant_ids": [], "description": "Random contest."},
        {"contest_name": "E", "created_date": "2024-04-15", "creator_id": "user123", "start_date": "2024-04-20", "final_date": "2024-05-20", "mindmap_ids": ["m5"], "participant_ids": ["p1","p2"], "description": "Random contest."},
        {"contest_name": "F", "created_date": "2024-03-12", "creator_id": "user123", "start_date": "2024-03-15", "final_date": "2024-04-15", "mindmap_ids": ["m4"], "participant_ids": [], "description": "Random contest."},
        {"contest_name": "G", "created_date": "2024-04-15", "creator_id": "user123", "start_date": "2024-04-20", "final_date": "2024-05-20", "mindmap_ids": ["m5"], "participant_ids": ["p1","p2"], "description": "Random contest."},
        {"contest_name": "H", "created_date": "2024-03-12", "creator_id": "user123", "start_date": "2024-03-15", "final_date": "2025-04-15", "mindmap_ids": ["m4"], "participant_ids": [], "description": "Random contest."},
        {"contest_name": "I", "created_date": "2024-04-15", "creator_id": "user123", "start_date": "2025-04-20", "final_date": "2025-05-20", "mindmap_ids": ["m5"], "participant_ids": [], "description": "Random contest."},
    ]
    
    # for Folders
    mock_folders_data = [
        {"folder_name": "A", "owner_id": "user123", "accessibility": True, "mindmap_ids": ["m1"]},
        {"folder_name": "B", "owner_id": "user123", "accessibility": True , "mindmap_ids": ["m2"]},
        {"folder_name": "C", "owner_id": "user123", "accessibility": True , "mindmap_ids": ["m4", "m1", "m2"]},
        {"folder_name": "D", "owner_id": "user123", "accessibility": True, "mindmap_ids": ["m4", "m1", "m2", "m3"]},
        {"folder_name": "E", "owner_id": "user123", "accessibility": True, "mindmap_ids": ["m5"]},
        {"folder_name": "F", "owner_id": "user123", "accessibility": True, "mindmap_ids": ["m4"]},
        {"folder_name": "G", "owner_id": "user123", "accessibility": True, "mindmap_ids": ["m5", "m1"]},
        {"folder_name": "H", "owner_id": "user123", "accessibility": True, "mindmap_ids": ["m4", "m1", "m2"]},
        {"folder_name": "I", "owner_id": "user456", "accessibility": True, "mindmap_ids": ["m5", "m1"]},
    ]
    
    @rx.var(cache=True)
    def filtered_and_sorted_mindmaps(self) -> List[dict]:
        # First filter
        mindmaps = self.all_mindmaps.copy()
        if self.search_query:
            mindmaps = [
                m for m in mindmaps 
                if self.search_query.lower() in m["mindmap_name"].lower()
            ]
        
        # Then sort
        if self.sort_option == "name_asc":
            mindmaps.sort(key=lambda x: x["mindmap_name"].lower())
        elif self.sort_option == "name_desc":
            mindmaps.sort(key=lambda x: x["mindmap_name"].lower(), reverse=True)
        elif self.sort_option == "date_asc":
            mindmaps.sort(key=lambda x: x["created_date"])
        elif self.sort_option == "date_desc":
            mindmaps.sort(key=lambda x: x["created_date"], reverse=True)
        elif self.sort_option == "num_terms_asc":
            mindmaps.sort(key=lambda x: x["terms"])
        elif self.sort_option == "num_terms_desc":
            mindmaps.sort(key=lambda x: x["terms"], reverse=True)

        return mindmaps
    
    @rx.var(cache=True)
    def filtered_and_sorted_contests(self) -> List[dict]:
        contests = [c for c in self.contests if c["status"] in {"Completed", "Locked", "In Progress"}]

        # Filter by search query
        if self.search_query:
            contests = [
                c for c in contests
                if self.search_query.lower() in c["contest_name"].lower()
            ]

        # Sort based on sort_option
        if self.sort_option == "name_asc":
            contests.sort(key=lambda x: x["contest_name"].lower())
        elif self.sort_option == "name_desc":
            contests.sort(key=lambda x: x["contest_name"].lower(), reverse=True)
        elif self.sort_option == "date_asc":
            contests.sort(key=lambda x: datetime.strptime(x["created_date"], "%Y-%m-%d"))
        elif self.sort_option == "date_desc":
            contests.sort(key=lambda x: datetime.strptime(x["created_date"], "%Y-%m-%d"), reverse=True)
        elif self.sort_option == "num_terms_asc":
            contests.sort(key=lambda x: len(x["mindmap_ids"]))
        elif self.sort_option == "num_terms_desc":
            contests.sort(key=lambda x: len(x["mindmap_ids"]), reverse=True)

        return contests
    
    @rx.var
    def bookmarked_mindmaps(self) -> List[dict]:
        bookmarked_ids = self.mock_user_data[0]["bookmark_mindmap"]

        # Filter only bookmarked mindmaps
        mindmaps = [
            m for m in self.mock_mindmaps_data
            if m["mindmap_id"] in bookmarked_ids
        ]

        # Apply search filter
        if self.search_query:
            mindmaps = [
                m for m in mindmaps
                if self.search_query.lower() in m["mindmap_name"].lower()
            ]

        # Apply sorting
        if self.sort_option == "name_asc":
            mindmaps.sort(key=lambda x: x["mindmap_name"].lower())
        elif self.sort_option == "name_desc":
            mindmaps.sort(key=lambda x: x["mindmap_name"].lower(), reverse=True)
        elif self.sort_option == "date_asc":
            mindmaps.sort(key=lambda x: x["created_date"])
        elif self.sort_option == "date_desc":
            mindmaps.sort(key=lambda x: x["created_date"], reverse=True)
        elif self.sort_option == "num_terms_asc":
            mindmaps.sort(key=lambda x: x["terms"])
        elif self.sort_option == "num_terms_desc":
            mindmaps.sort(key=lambda x: x["terms"], reverse=True)

        return mindmaps

        
    def set_search_query(self, query: str):
        self.search_query = query
    
    def set_sort_option(self, value: str):
        self.sort_option = value
        self.sort_refresh = not self.sort_refresh  # Trigger UI refresh
        
    def set_active_tab(self, tab: str):
        self.active_tab = tab

    def open_mindmap(self, mindmap_id: str, mindmap_name: str):
        pass

    def load_library_data(self):
        try:
            self.all_mindmaps = [m for m in self.mock_mindmaps_data if m["creator_id"] == self.user_id]
            today = datetime.today().date()

            self.contests = []
            for c in self.mock_contests_data:
                if c["creator_id"] != self.user_id:
                    continue

                start_date = datetime.strptime(c["start_date"], "%Y-%m-%d").date()
                final_date = datetime.strptime(c["final_date"], "%Y-%m-%d").date()

                if today < start_date:
                    status = "Locked"
                elif today > final_date:
                    status = "Completed"
                else:
                    status = "In Progress"

                self.contests.append({
                    **c,
                    "participant_count": sum(1 for _ in c["participant_ids"]),
                    "status": status
                })

        except Exception as e:
            self.error_message = f"An error occurred: {str(e)}"

    def open_mindmap(self, mindmap_id: str, mindmap_name: str):
        self.error_message = f"Opening mindmap: {mindmap_name} (ID: {mindmap_id})"
        
    def open_contest(self, contest_id: str, contest_name: str):
        self.error_message = f"Opening contest: {contest_name} (ID: {contest_id})"
        
class CreateFolderState(rx.State):
    user_id: str = "user123"
    folder_name: str = ""
    folders: List[dict] = []
    error_message: str = ""
    selected_mindmaps: List[dict] = []
    show_modal: bool = False
    show_mindmap_list: bool = False
    
    available_mindmaps: List[dict] = [
        {"mindmap_id": "m1", "mindmap_name": "Python Basics", "created_date": "2024-01-10", "creator_id": "user123", "accessibility": True, "terms": 10},
        {"mindmap_id": "m2", "mindmap_name": "Data Structures", "created_date": "2024-02-05", "creator_id": "user123", "accessibility": True, "terms": 20},
        {"mindmap_id": "m3", "mindmap_name": "React Concepts", "created_date": "2024-03-15", "creator_id": "user456", "accessibility": True, "terms": 40},
    ]
    
    def is_selected(self, mindmap: dict) -> bool:
        return any(m["mindmap_id"] == mindmap["mindmap_id"] for m in self.selected_mindmaps)

    def set_folder_name(self, name: str):
        self.folder_name = name.strip()
        self.error_message = ""
        
    def toggle_mindmap_list(self):
        self.show_mindmap_list = not self.show_mindmap_list

    def toggle_mindmap_selection_by_id(self, mindmap_id: str):
        mindmap = next((m for m in self.available_mindmaps if m["mindmap_id"] == mindmap_id), None)
        if not mindmap:
            return
        if mindmap in self.selected_mindmaps:
            self.selected_mindmaps.remove(mindmap)
        else:
            self.selected_mindmaps.append(mindmap)

    def is_selected(self, mindmap: dict) -> bool:
        return any(m["mindmap_id"] == mindmap["mindmap_id"] for m in self.selected_mindmaps)

    @rx.var
    def get_selected_mindmap_count(self) -> int:
        """Return the number of selected mindmaps in the folder."""
        return len(self.selected_mindmaps)
    
    def reset_form(self):
        """Reset all form fields and states"""
        self.folder_name = ""
        self.selected_mindmaps = []
        self.error_message = ""
        self.show_mindmap_list = False
            
    @rx.event
    async def create_folder(self):
        if not self.folder_name:
            self.error_message = "Folder name cannot be empty"
            return

        new_folder = {
            "folder_name": self.folder_name,
            "owner_id": self.user_id,
            "accessibility": True,
            "mindmap_ids": [m["mindmap_id"] for m in self.selected_mindmaps]
        }
        
        print("🔹 Sending payload:", new_folder)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/folders/",
                    json=new_folder
                )

            if response.status_code == 200:
                self.folders.append(new_folder)
                self.reset_form()
            
            else:
                self.error_message = f"Failed to create folder: {response.text}"

        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            
    @rx.event
    async def load_folders(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/folders/")
            if response.status_code == 200:
                self.folders = response.json()
            else:
                self.error_message = f"Failed to fetch folders: {response.text}"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"

