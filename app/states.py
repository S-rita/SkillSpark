import reflex as rx
import httpx
from typing import Optional, List, Dict, Any
import calendar
from datetime import date, timedelta, datetime

class LoginState(rx.State):
    username: str = ""
    password: str = ""
    login_error: str = ""
    is_logged_in: bool = False
    user_id: str = ""
    _current_user_id = ""
    
    # Add a class var to make user_id accessible to other states
    @classmethod
    def get_user_id(cls):
        """Class method to get the current user ID"""
        return cls._current_user_id
    
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
                    
                    # Update state
                    self.login_error = ""
                    self.is_logged_in = True
                    self.user_id = result.get("user_id", "")
                    LoginState._current_user_id = self.user_id
                    
                    yield rx.window_alert("login successful!")
                    yield rx.redirect("/main")  # Redirect properly
                else:
                    # Handle login error
                    result = response.json()
                    self.login_error = result.get("detail", "Invalid username or password")
        
        except Exception as e:
            self.login_error = f"An error occurred: {str(e)}"
    
    async def logout(self):
        """Handle user logout."""
        self.is_logged_in = False
        self.username = ""
        self.password = ""
        self.user_id = ""
        LoginState._current_user_id = ""
        
        rx.redirect("/")

    
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
                    json={"username": self.username, "password": self.password, "email": self.email}
                )

                if response.status_code == 200:
                    result = response.json()

                    # Update both SignupState and LoginState
                    self.signup_error = ""
                    self.is_signed_up = True

                    # Automatically log in the user after successful signup
                    LoginState.is_logged_in = True
                    LoginState.user_id = result.get("user_id", "")
                    LoginState.username = self.username  # Optional

                    yield rx.window_alert("Signup successful!")
                    yield rx.redirect("/main")  # Redirect properly
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

class MindMapState(rx.State):
    mindmap: Dict[int, Dict[str, Any]] = {
        0: {"text": "Root", "parent": None, "depth": 0},
        1: {"text": "Child", "parent": 0, "depth": 1},
        2: {"text": "GrandChild", "parent": 1, "depth": 2},
        3: {"text": "GreatGrandChild", "parent": 2, "depth": 3}
    }
    mindmap_name: str = "Untitled MindMap"
    mindmap_description: str = ""
    mindmap_id: Optional[str] = None
    creator_id: Optional[str] = None
    is_saving: bool = False
    save_message: str = ""
    save_error: bool = False
    update_counter: int = 0
    editing_node_id: Optional[int] = None
    editing_text: str = ""

    async def on_load(self):
        """Set creator_id from login state when page loads"""
        login_state = LoginState.get_current()
        if login_state.is_logged_in:
            self.creator_id = login_state.user_id
    def start_editing(self, node_id: int):
        self.editing_node_id = node_id
        self.editing_text = self.mindmap[node_id]["text"]

    def save_editing(self):
        if self.editing_node_id is not None:
            self.update_node_text(self.editing_node_id, self.editing_text)
            self.editing_node_id = None
            self.editing_text = ""

    def cancel_editing(self):
        self.editing_node_id = None
        self.editing_text = ""

    def handle_edit_change(self, value: str):
        self.editing_text = value

    @rx.var(cache=True)
    def get_mindmap(self) -> Dict[int, Dict[str, Any]]:
        _ = self.update_counter
        return {k: v.copy() for k, v in self.mindmap.items()}
    
    @rx.var(cache=True)
    def get_children(self) -> Dict[int, List[int]]:
        _ = self.update_counter
        
        children = {}
        for node_id in self.mindmap:
            children[node_id] = []
            
        for node_id, node_data in self.mindmap.items():
            parent_id = node_data.get("parent")
            if parent_id is not None and parent_id in children:
                children[parent_id].append(node_id)
                
        return children
    
    @rx.var(cache=True)
    def get_root_nodes(self) -> List[int]:
        _ = self.update_counter
        
        return [node_id for node_id, data in self.mindmap.items() 
                if data.get("parent") is None]
    
    @rx.var(cache=True)
    def get_display_order(self) -> List[int]:

        _ = self.update_counter
        
        def traverse(node_id: int, order: List[int]):
            order.append(node_id)  # Add the current node first
            for child_id in self.get_children.get(node_id, []):  # Get children safely
                traverse(child_id, order)  # Recursively add child nodes

        display_order = []
        for root_id in self.get_root_nodes:  # Start with root nodes
            traverse(root_id, display_order)

        return display_order

    def trigger_update(self):
        """Increment counter to force re-rendering"""
        self.update_counter += 1

    def add_child(self, parent_id: int = None):
        """Add a new child node dynamically."""
        new_id = max(self.mindmap.keys(), default=-1) + 1
        parent_depth = self.mindmap[parent_id]["depth"] if parent_id in self.mindmap else -1
        
        self.mindmap[new_id] = {
            "text": f"Node {new_id}", 
            "parent": parent_id,
            "depth": parent_depth + 1 if parent_id is not None else 0
        }
        
        self.trigger_update()

    def delete_node(self, node_id: int):
        """Delete a node and its children recursively."""
        if node_id not in self.mindmap:
            return

        children_to_delete = []
        for child_id, child_data in self.mindmap.items():
            if child_data.get("parent") == node_id:
                children_to_delete.append(child_id)
        
        for child_id in children_to_delete:  
            child_children = [cid for cid, data in self.mindmap.items() 
                            if data.get("parent") == child_id]
            for gc in child_children:
                self.delete_node(gc)
            if child_id in self.mindmap:
                del self.mindmap[child_id]
        
        del self.mindmap[node_id]
        self.trigger_update()
    
    def update_node_text(self, node_id: int, text: str):
        """Update the text of a node."""
        if node_id in self.mindmap:
            self.mindmap[node_id]["text"] = text
            self.trigger_update()
    
    def change_parent(self, node_id: int, new_parent_id: Optional[int]):
        """Change the parent of a node."""
        if node_id not in self.mindmap:
            return
            
        if new_parent_id is not None:
            current = new_parent_id
            while current is not None:
                if current == node_id:
                    return
                parent_data = self.mindmap.get(current)
                if not parent_data:
                    break
                current = parent_data.get("parent")
        
        self.mindmap[node_id]["parent"] = new_parent_id
        
        if new_parent_id is None:
            new_depth = 0
        else:
            new_depth = self.mindmap[new_parent_id]["depth"] + 1
        
        self.mindmap[node_id]["depth"] = new_depth
        
        self._update_descendants_depth(node_id, new_depth)
        
        self.trigger_update()
    
    def _update_descendants_depth(self, node_id: int, parent_depth: int):
        """Recursively update the depth of all descendants."""
        children = []
        for cid, data in self.mindmap.items():
            if data.get("parent") == node_id:
                children.append(cid)
        
        for child_id in children:
            new_depth = parent_depth + 1
            self.mindmap[child_id]["depth"] = new_depth
            self._update_descendants_depth(child_id, new_depth)
    
    async def handle_createMindMap(self):
        self.is_saving = True
        self.save_message = "Saving topics and mindmap..."
        self.save_error = False

        self.creator_id = LoginState.get_user_id()
            
        # If still no user ID, show error
        if not self.creator_id:
            self.save_message = "You must be logged in to save a MindMap"
            self.save_error = True
            self.is_saving = False
            return
        
        # Dictionary to store the mapping between local node IDs and backend topic IDs
        node_to_topic_id = {}
        
        try:
            # First pass: Create all topics WITHOUT parent relationships
            for node_id, node_data in self.mindmap.items():
                async with httpx.AsyncClient() as client:
                    topic_data = {
                        "topic_name": node_data["text"],
                        "description": "Topic from mindmap",
                        "depth": node_data["depth"],
                        "parent_id": None  # Initially set all parent_ids to null
                    }
                    
                    response = await client.post(
                        "http://localhost:8000/topics/",
                        json=topic_data,
                    )
                    
                    if response.status_code in [200, 201]:
                        data = response.json()
                        topic_id = data.get("topic_id")
                        
                        if not topic_id:
                            self.save_message = f"Error extracting topic ID from response: {data}"
                            self.save_error = True
                            self.is_saving = False
                            return
                        
                        # Store mapping between node_id and backend topic_id
                        node_to_topic_id[node_id] = topic_id
                        print(f"Created topic for node {node_id}: {topic_id}")
                    else:
                        self.is_saving = False
                        self.save_message = f"Error creating topic: {response.status_code} - {response.text}"
                        self.save_error = True
                        return
            
            # Second pass: Update parent relationships
            for node_id, node_data in self.mindmap.items():
                parent_id = node_data.get("parent")
                
                # Only update topics that have parents
                if parent_id is not None and parent_id in node_to_topic_id:
                    # Get the backend topic IDs
                    topic_id = node_to_topic_id.get(node_id)
                    parent_topic_id = node_to_topic_id.get(parent_id)
                    
                    print(f"Updating topic {topic_id} with parent {parent_topic_id}")
                    
                    # Create a new topic with the updated parent_id
                    async with httpx.AsyncClient() as client:
                        # Using POST to create a new topic with the same name but updated parent
                        response = await client.post(
                            "http://localhost:8000/topics/update_parent",
                            json={
                                "topic_id": topic_id,
                                "parent_id": parent_topic_id
                            }
                        )
                        
                        if response.status_code != 200:
                            print(f"Warning: Failed to update parent relationship: {response.status_code} - {response.text}")
                            # Continue anyway - we'll still create the mindmap
            
            # Finally, create the mindmap with all topic IDs
            topic_ids = list(node_to_topic_id.values())
            print(f"Creating mindmap with topic_ids: {topic_ids}")
            print(f"Creating mindmap with topic_ids: {self.creator_id}")
            
            mindmap_data = {
                "mindmap_name": self.mindmap_name,
                "mindmap_description": self.mindmap_description,
                "creator_id": self.creator_id or "default_user",
                "accessibility": not getattr(self, "access_private", True),  # Assuming AccessButtonToggle.private
                "topic_ids": topic_ids
            }
            
            # Add description if it exists
            if hasattr(self, "mindmap_description") and self.mindmap_description:
                mindmap_data["description"] = self.mindmap_description
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/mindmaps/",
                    json=mindmap_data,
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    mindmap_id = data.get("mindmap_id")
                    
                    if mindmap_id:
                        self.mindmap_id = mindmap_id
                        self.is_saving = False
                        self.save_message = f"MindMap saved successfully!"
                        self.save_error = False
                        
                        # Reset the mindmap to default state
                        self.reset_mindmap()
                        
                        # Redirect to the mindmap page
                        return rx.redirect(f"/mindmap")
                    else:
                        self.is_saving = False
                        self.save_message = f"MindMap created but couldn't extract ID. Response: {data}"
                        self.save_error = True
                else:
                    self.is_saving = False
                    self.save_message = f"Error creating mindmap: {response.status_code} - {response.text}"
                    self.save_error = True
                    
        except Exception as e:
            self.is_saving = False
            self.save_message = f"Error in save process: {str(e)}"
            self.save_error = True
            import traceback
            print(f"Exception details: {traceback.format_exc()}")

    def reset_mindmap(self):
        """Reset the mindmap to its default state after successful creation."""
        # Reset to default structure
        self.mindmap = {
            0: {"text": "Root", "parent": None, "depth": 0},
            1: {"text": "Child", "parent": 0, "depth": 1},
            2: {"text": "GrandChild", "parent": 1, "depth": 2},
            3: {"text": "GreatGrandChild", "parent": 2, "depth": 3}
        }
        
        # Reset other properties
        self.mindmap_name = "Untitled MindMap"
        self.mindmap_description = ""
        self.editing_node_id = None
        self.editing_text = ""
        self.mindmap_id = None
        
        # Force update
        self.trigger_update()

class Main_Pages_state(rx.State):
    search_text: str = ""
    display_text: str = ""  # Store the displayed text
    filtered_mindmaps: list[dict] = []  # New state var for filtered results#!!!!!
    filtered_contests: list[dict] = []  # New state var for filtered contests#!!!!!


    # Add state var to track view on search page when click "view more" button
    show_mindmaps_full: bool = False
    show_contests_full: bool = False

    def toggle_mindmaps_view(self):
        self.show_mindmaps_full = not self.show_mindmaps_full
        self.show_contests_full = False  # Reset other view

    def toggle_contests_view(self):
        self.show_contests_full = not self.show_contests_full
        self.show_mindmaps_full = False  # Reset other view


    # Add a state variable to track the search results is it have mind map > 3 if yes show "view more" button
    @rx.var
    def has_more_mindmaps(self) -> bool:
        return len(self.filtered_mindmaps) > 3
    
    # Add a state variable to track the search results is it have contest > 3 if yes show "view more" button
    @rx.var
    def has_more_contests(self) -> bool:
        return len(self.filtered_contests) > 3
        
    #for Slide show##########################################
    current_index: int = 0  # Track current position

    @rx.var
    def visible_mindmaps(self) -> list[dict]:
        # Show 3 mindmaps at a time starting from current_index
        return self.favorite_mindmaps[self.current_index:self.current_index + 3]
    
    @rx.var
    def can_go_next(self) -> bool:
        return self.current_index + 3 < len(self.favorite_mindmaps)
    
    @rx.var 
    def can_go_prev(self) -> bool:
        return self.current_index > 0
        
    def next_slide(self):
        if self.can_go_next:
            self.current_index += 3
            
    def prev_slide(self):
        if self.can_go_prev:
            self.current_index -= 3
    ###################################################

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
        "username": "Asayaa",  # Default user name
        "email": "66011148@kmitl.ac.th",
        "password": "12345678",
        "bookmark_mindmap" : [],
        "achievements_ids": [],
        "user_id": "1234567890",
        "image": "/prettestGirlInDaWorldo.png"
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
            "image": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "terms": 12, 
            "creator": "Khaopun",
            "image": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "idk",
            "terms": 24,
            "creator": "Bew",
            "image": "/static/logo.png" 
        }
    ]

    # Top creators data
    top_creators: list[dict] = [
        {
            "name": "Prang",
            "mindmap_count": 12,
            "contest_count": 5,
            "image": "/static/logo.png"
        },
        {
            "name": "karina",
            "mindmap_count": 5,
            "contest_count": 2,
            "image": "/static/logo.png"
        },
        {
            "name": "AsaBm",
            "mindmap_count": 122,
            "contest_count": 52,
            "image": "/static/logo.png"
        }
    ]

    # all mindmaps data 
    Mind_map: list[dict] = [
        {
            "name": "Python is the Best",
            "terms": 27,
            "creator": "Prang",
            "image": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "terms": 12, 
            "creator": "Khaopun",
            "image": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "oyh",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "asaaaa",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        }
    ]

    # all contests data 
    Contest: list[dict] = [
        {
            "name": "Python is the Best",
            "sets": 27,
            "creator": "Prang",
            "image": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "sets": 12, 
            "creator": "Khaopun",
            "image": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "sets": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "C++ for u",
            "sets": 5,
            "creator": "bbeee",
            "image": "/static/logo.png" 
        }
    ]


#????? achievements page
#????? Achievements data use  name, image, category, completion,
class Achiecement_State(rx.State):
    """The app state."""
    # Achievement data structure based on your Achievement model
    achievements: list[dict] = [
        # Best of the best achievements
        {
            "id": "perfectionist",
            "name": "Perfectionist",
            "image": "/Perfectionist.png",
            "category": "best",
            "completion": True,
            # "description": "Get 100% on a mindmap"
        },
        {
            "id": "chicken_dinner", 
            "name": "Chicken dinner",
            "image": "/Chicken_dinner.png",
            "category": "best",
            "completion": True,
            # "description": "Win first place in a contest"
        },
        {
            "id": "one_take_wonder",
            "name": "One-Take Wonder", 
            "image": "/One_take_Wonder.png",
            "category": "best",
            "completion": True,
            # "description": "Complete a mindmap perfectly on first try"
        },

        # One step ahead achievements
        {
            "id": "mind_mapper",
            "name": "Mind Mapper",
            "image": "/Mind_Mapper.png", 
            "category": "neutral",
            "completion": False,
            # "description": "Create your first mindmap"
        },
        {
            "id": "brave_entry",
            "name": "Brave Entry",
            "image": "/Brave_Entry.png",
            "category": "neutral", 
            "completion": True,
            # "description": "Enter your first contest"
        },
        {
            "id": "creative_flow",
            "name": "Creative Flow",
            "image": "/Creative_Flow.png",
            "category": "neutral",
            "completion": False,
            # "description": "Create 5 mindmaps"
        },
        {
            "id": "first_step",
            "name": "First Step",
            "image": "/First_Step.png",
            "category": "neutral",
            "completion": True,
            # "description": "Complete your first mindmap"
        },
        {
            "id": "back_on_track",
            "name": "Back on Track",
            "image": "/Back_on_Track.png",
            "category": "neutral",
            "completion": True,
            # "description": "Resume learning after a break"
        },

        # Best of the worst achievements
        {
            "id": "epic_oops",
            "name": "Epic Oops",
            "image": "/Epic_Oops.png",
            "category": "worst",
            "completion": False,
            # "description": "Get 0% on a mindmap"
        },
        {
            "id": "better_luck",
            "name": "Better Luck Next Time",
            "image": "/Better_Luck_Next_Time.png",
            "category": "worst",
            "completion": False,
            # "description": "Fail a contest"
        },

        # Daily streak achievements
        {
            "id": "triple_flame",
            "name": "Triple Flame",
            "image": "/Triple_Flame.png",
            "category": "daily",
            "completion": False,
            # "description": "3 day streak"
        },
        {
            "id": "high_five",
            "name": "High Five Hustler",
            "image": "/High_Five_Hustler.png",
            "category": "daily",
            "completion": False,
            # "description": "5 day streak"
        },
        {
            "id": "tenacious",
            "name": "Tenacious Ten",
            "image": "/Tenacious_Ten.png",
            "category": "daily",
            "completion": False,
            # "description": "10 day streak"
        },
        {
            "id": "power_twenty",
            "name": "Power of Twenty",
            "image": "/Power_of_Twenty.png",
            "category": "daily",
            "completion": False,
            # "description": "20 day streak"
        },
        {
            "id": "thirty_titan",
            "name": "Thirty Day Titan",
            "image": "/Thirty_Day_Titan.png",
            "category": "daily",
            "completion": True,
            # "description": "30 day streak"
        }
    ]

    @rx.var
    def best_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "best"]
    
    @rx.var
    def neutral_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "neutral"]
    
    @rx.var 
    def worst_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "worst"]
    
    @rx.var
    def daily_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "daily"]
    
    @rx.var
    def completed_count(self) -> int:
        return len([a for a in self.achievements if a["completion"] == True])
    
    @rx.var 
    def user_level(self) -> str:
        if self.completed_count <= 5:
            return "Novice"
        elif self.completed_count <= 10:
            return "Competent"  
        elif self.completed_count <= 14:
            return "Master"
        else:
            return "Legend"
        
    @rx.var
    def level_image(self) -> str:
        if self.completed_count <= 5:
            return "/egg.png"
        elif self.completed_count <= 10:
            return "/eggChic.png"
        elif self.completed_count <= 14:
            return "/Chic.png"
        else:
            return "/chicOld.png"
        
#????? calendar page
#????? Calendar data use date that has login in form of like login_dates: list[dict]

class CalendarState(rx.State):
    current_month: int = datetime.now().month
    current_year: int = datetime.now().year
    login_dates: list[dict] = [
        {"date": date(current_year, 1, 5), "has_login": True},
        {"date": date(current_year, 1, 6), "has_login": True},
        {"date": date(current_year, 1, 15), "has_login": True},
        {"date": date(current_year, 1, 16), "has_login": True},
        {"date": date(current_year, 1, 25), "has_login": True},
        {"date": date(current_year, 2, 1), "has_login": True},
        {"date": date(current_year, 2, 9), "has_login": True},
        {"date": date(current_year, 2, 10), "has_login": True},
        {"date": date(current_year, 2, 11), "has_login": True},
        {"date": date(current_year, 2, 20), "has_login": True},
        {"date": date(current_year, 2, 28), "has_login": True},
        {"date": date(current_year, 3, 5), "has_login": True},
        {"date": date(current_year, 3, 10), "has_login": True},
        {"date": date(current_year, 3, 15), "has_login": True},
        {"date": date(current_year, 3, 20), "has_login": True},
        {"date": date(current_year, 3, 21), "has_login": True},
        {"date": date(current_year, 3, 25), "has_login": True},
        {"date": date(current_year, 3, 31), "has_login": True},
        {"date": date(current_year, 4, 1), "has_login": True},
    ]

    @rx.var
    def current_streak(self) -> tuple[str, int]:
        """Get current streak of consecutive days ending with today."""
        today = datetime.now()
        
        # Get all login dates for current month and year
        current_streak = 0
        
        # Get all login dates sorted by date
        login_dates = sorted([
            d["date"] 
            for d in self.login_dates
        ], reverse=True)
        
        # Find consecutive days ending with today
        for date in login_dates:
            if date == today.date():
                current_streak = 1
                prev_date = today.date() - timedelta(days=1)
                
                # Check previous consecutive days
                while prev_date in [d["date"] for d in self.login_dates]:
                    current_streak += 1
                    prev_date -= timedelta(days=1)
                break
        
        # Format text based on streak
        if current_streak == 0:
            return "0 day streak", 0
        elif current_streak == 1:
            return "1 day streak", 1
        else:
            return f"{current_streak} days streak", current_streak
        

    @rx.var
    def streak_image(self) -> str:
        """Get streak image based on current streak."""
        _, streak = self.current_streak
        
        if streak == 1:
            return "/lowCostFire.png"
        else:
            return "/Fire_lowBG.png"

    # Add a new method to check if a day is part of consecutive days
    @rx.var
    def is_consecutive_day(self) -> list[int]:
        """Get all days that are part of consecutive sequences"""
        current_month_dates = sorted([
            d["date"] 
            for d in self.login_dates 
            if (d["date"].month == self.current_month and d["date"].year == self.current_year) or
            (d["date"].month == self.current_month-1 and d["date"].year == self.current_year and d["date"].day == 31) or
            (self.current_month == 1 and d["date"].month == 12 and d["date"].year == self.current_year-1 and d["date"].day == 31)
        ])
        
        next_month_dates = sorted([
            d["date"]
            for d in self.login_dates
            if ((d["date"].month == self.current_month+1 and d["date"].year == self.current_year and d["date"].day == 1) or
                (self.current_month == 12 and d["date"].month == 1 and d["date"].year == self.current_year+1 and d["date"].day == 1))
        ])
        
        # Combine the dates
        all_relevant_dates = sorted(current_month_dates + next_month_dates)
        
        consecutive_days = []
        current_group = []
        
        for i in range(len(all_relevant_dates)):
            if not current_group:
                current_group.append(all_relevant_dates[i])
            elif (all_relevant_dates[i] - current_group[-1]).days == 1:
                current_group.append(all_relevant_dates[i])
            else:
                if len(current_group) > 1:
                    consecutive_days.extend([d.day for d in current_group if d.month == self.current_month])
                current_group = [all_relevant_dates[i]]
        
        if len(current_group) > 1:
            consecutive_days.extend([d.day for d in current_group if d.month == self.current_month])
            
        return consecutive_days

    

    

    @rx.var
    def dates_in_current_month(self) -> list[str]:
        """Get login dates for current month as strings"""
        return [
            str(d["date"].day)
            for d in self.login_dates 
            if d["date"].month == self.current_month and 
                d["date"].year == self.current_year
        ]
    
    def next_month(self):
        # Only allow going forward if not at current month/year
        if (self.current_month < datetime.now().month or 
            self.current_year < datetime.now().year):
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
            
    def prev_month(self):
        # Only allow going back if not at January of current year
        if self.current_month > 1 and self.current_year == datetime.now().year:
            self.current_month -= 1

    @rx.var
    def month_name(self) -> str:
        return calendar.month_name[int(self.current_month)]
    
    @rx.var
    def can_go_forward(self) -> bool:
        return (self.current_month < datetime.now().month or 
                self.current_year < datetime.now().year)

    @rx.var
    def can_go_back(self) -> bool:
        return self.current_month > 1 and self.current_year == datetime.now().year
    
    @rx.var
    def days_in_month(self) -> int:
        return calendar.monthrange(self.current_year, self.current_month)[1]
    
    @rx.var
    def prev_month_days(self) -> int:
        if self.current_month == 1:
            return calendar.monthrange(self.current_year - 1, 12)[1]
        return calendar.monthrange(self.current_year, self.current_month - 1)[1]
    
    @rx.var
    def first_day_offset(self) -> int:
        # January starts on Wednesday (3)
        if self.current_month == 1:
            return 3
        
        # Calculate cumulative days to determine first day of other months
        total_days = 3  # Start from Wednesday
        for month in range(1, self.current_month):
            total_days += calendar.monthrange(self.current_year, month)[1]
        return total_days % 7