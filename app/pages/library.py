import reflex as rx
from typing import List
from app.components import sidebar
from datetime import datetime
import httpx

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
        
# ---- Search & Filter ----
def search_and_filter() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Search mindmaps, contests...",
            on_change=Library.set_search_query,
            value=Library.search_query,
            width="80%",
            height="50px",
            background_color="white",
            color="black",
            font_size="1.1em",
            style={"& input::placeholder": {"color": "#919191"}}
        ),
        rx.menu.root(
            rx.menu.trigger(
                rx.button("Sort By", variant="soft", height="50px", width="100px", font_size="1.1em"),
            ),
            rx.menu.content(
                rx.menu.item("Name (A-Z)", on_click=lambda: Library.set_sort_option("name_asc")),
                rx.menu.item("Name (Z-A)", on_click=lambda: Library.set_sort_option("name_desc")),
                rx.menu.separator(),
                rx.menu.item("Date (Oldest First)", on_click=lambda: Library.set_sort_option("date_asc")),
                rx.menu.item("Date (Newest First)", on_click=lambda: Library.set_sort_option("date_desc")),
                rx.menu.separator(),
                rx.menu.item("Number of Terms (Least)", on_click=lambda: Library.set_sort_option("num_terms_asc")),
                rx.menu.item("Number of Terms (Most)", on_click=lambda: Library.set_sort_option("num_terms_desc")),
            )
        ),
        width="100%",
        spacing="4",
    )

# ---- Main Page ----
def library_page() -> rx.Component:
    return rx.hstack( 
        sidebar(), 

        rx.box( 
            rx.vstack(
                rx.heading("Your Library", font_size="80px", margin_bottom="50px", color="black", margin_top="60px"),
                search_and_filter(), 
                rx.text(Library.error_message, color="red"),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Mindmaps", value="mindmaps", color="black", font_size="1.5em", margin_right="50px", margin_bottom="20px"),
                        rx.tabs.trigger("Contests", value="contests", color="black", font_size="1.5em", margin_bottom="20px", margin_right="50px"),
                        rx.tabs.trigger("Folders", value="folders", color="black", font_size="1.5em", margin_bottom="20px", margin_right="50px"),
                        rx.tabs.trigger("Bookmarks", value="bookmarks", color="black", font_size="1.5em", margin_bottom="20px", margin_right="50px"),
                    ),
                    rx.tabs.content(
                        mindmaps_view(),
                        value="mindmaps",
                        margin_top="20px",
                    ),
                    rx.tabs.content(
                        contests_view(),
                        value="contests",
                        margin_top="20px",
                    ),
                    rx.tabs.content(
                        folders_view(),
                        value="folders",
                        margin_top="20px",
                    ),
                    rx.tabs.content(
                        bookmarks_view(),
                        value="bookmarks",
                        margin_top="20px",
                    ),
                    default_value="mindmaps", # for convenient
                    on_change=Library.set_active_tab,
                    on_mount=Library.load_library_data
                ),
            ),
            background_color="#fffbe6",
            padding="40px",
            height="100vh", 
            overflow_y="auto",
            flex="1",
        ),
        align="start",
        spacing="0",
    )

# ---- Mind Map View ----
def mindmaps_view() -> rx.Component:
    return rx.grid(
        rx.foreach(
            Library.filtered_and_sorted_mindmaps,
            lambda m: rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.image(src="/tree.png", width="70px", height="60px", margin_top="10px", margin_left="10px"),
                        rx.text(m["mindmap_name"], font_size="1.2em", font_weight="bold", color="black", margin_top="20px", margin_left="10px"),
                    ),
                    rx.spacer(),
                    rx.cond(
                        m["creator_id"] == Library.user_id,
                        rx.hstack(
                            rx.text(f"created on: {m['created_date']}", margin_right="60px"),
                            rx.box(
                                rx.text(f"{m['terms']} terms"),
                                padding_x="18px",
                                padding_y="2px",
                                background_color="#FFF5D0",
                                border_radius="12px",
                                font_size="0.9em",
                                font_weight="medium"
                            ),
                            color="black",
                            margin_top="15px",
                            margin_left="20px",
                        )
                    ),
                ),
                padding="16px",
                background_color="#FDE68A",
                border_radius="16px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                width="400px",
                height="170px",
                margin_top="10px",
                cursor="pointer",
                margin_bottom="10px",
                on_click=lambda m=m: Library.open_mindmap(m["mindmap_id"], m["mindmap_name"])
            )
        ),
        columns="3",
        spacing="6",
        width="100%"
    )

# ---- Contest View ----
def contests_view() -> rx.Component:
    return rx.grid(
        rx.foreach(
            Library.filtered_and_sorted_contests,
            lambda c: rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.image(src="/contest.svg", width="70px", height="60px", margin_top="10px", margin_left="10px"),
                        rx.text(c["contest_name"], font_size="1.2em", font_weight="bold", color="black", margin_top="20px", margin_left="10px"),
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.text(f"Status: {c['status']}", color="black", margin_right="100px"),
                        rx.box(
                            rx.text(f"{c['participant_count']} joined"),
                            padding_x="18px",
                            padding_y="2px",
                            background_color="#FFF5D0",
                            border_radius="12px",
                            font_size="0.9em",
                            font_weight="medium"
                        ),
                        color="black",
                        margin_top="15px",
                        margin_left="20px",
                    )
                ),
                padding="16px",
                background_color="#FDE68A",
                border_radius="16px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                width="400px",
                height="170px",
                margin_top="10px",
                margin_bottom="10px",
                cursor="pointer",
                on_click=lambda c=c: Library.open_contest(c["contest_id"], c["contest_name"])
            )
        ),
        columns="3",
        spacing="6",
        width="100%"
    )

# ---- Bookmark View ----
def bookmarks_view() -> rx.Component:
    return rx.grid(
        rx.foreach(
            Library.bookmarked_mindmaps,
            lambda m: rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.image(
                            src="/tree.png",
                            width="70px",
                            height="60px",
                            margin_top="10px",
                            margin_left="10px"
                        ),
                        rx.text(
                            m["mindmap_name"],
                            font_size="1.2em",
                            font_weight="bold",
                            color="black",
                            margin_top="20px",
                            margin_left="10px"
                        ),
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.text(f"created on: {m['created_date']}", margin_right="60px"),
                        rx.box(
                            rx.text(f"{m['terms']} terms"),
                            padding_x="18px",
                            padding_y="2px",
                            background_color="#FFF5D0",
                            border_radius="12px",
                            font_size="0.9em",
                            font_weight="medium"
                        ),
                        color="black",
                        margin_top="15px",
                        margin_left="20px",
                    )
                ),
                padding="16px",
                background_color="#FDE68A",
                border_radius="16px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                width="400px",
                height="170px",
                margin_top="10px",
                margin_bottom="10px",
                cursor="pointer",
                on_click=lambda m=m: Library.open_mindmap(
                    m["mindmap_id"],
                    m["mindmap_name"]
                )
            )
        ),
        columns="3",
        spacing="6",
        width="100%"
    )


class CreateFolderState(rx.State):
    user_id: str = "user123"
    folder_name: str = ""
    folders: List[dict] = []
    error_message: str = ""
    selected_mindmaps: List[dict] = []
    show_modal: bool = False
    show_mindmap_list: bool = False

    available_mindmaps = [
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

    def toggle_mindmap_selection(self, mindmap_id: str):
        mindmap = next((m for m in self.available_mindmaps if m["mindmap_id"] == mindmap_id), None)
        if not mindmap:
            return
        
        if any(m["mindmap_id"] == mindmap_id for m in self.selected_mindmaps):
            self.selected_mindmaps = [m for m in self.selected_mindmaps if m["mindmap_id"] != mindmap_id]
        else:
            self.selected_mindmaps.append(mindmap)

    @rx.event
    async def submit_folder(self):
        if not self.folder_name:
            self.error_message = "Folder name cannot be empty"
            return

        new_folder = {
            "folder_name": self.folder_name,
            "owner_id": self.user_id,
            "accessibility": True,
            "mindmap_ids": [m["mindmap_id"] for m in self.selected_mindmaps]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/folders/",
                    json=new_folder
                )

            if response.status_code == 200:
                self.folders.append(new_folder)
                self.folder_name = ""
                self.selected_mindmaps = []
                self.error_message = ""
                self.show_modal = False
            else:
                self.error_message = f"Failed to create folder: {response.text}"

        except Exception as e:
            self.error_message = f"Error: {str(e)}"

def folders_view() -> rx.Component:
    return rx.box(
        rx.dialog.root(
            rx.dialog.trigger(
                rx.box(
                    rx.center(
                        rx.button(
                            "+",
                            font_size="100px",
                            font_weight="bold",
                            background_color="#B1A16B", 
                            color="#FFFFFF",
                            border_radius="12px",
                            height="100px",
                            width="100px",
                        )
                    ),
                    padding="16px",
                    background_color="#B1A16B",
                    border_radius="16px", 
                    box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                    width="400px",
                    height="170px",
                    margin_top="10px",
                    margin_bottom="10px",
                    cursor="pointer"
                )
            ),
            rx.dialog.content(
                rx.vstack(
                    rx.text("Create New Folder", font_size="1.5em", font_weight="bold", color="black"),
                    rx.input(
                        placeholder="Enter folder name",
                        value=CreateFolderState.folder_name,
                        on_change=CreateFolderState.set_folder_name,
                        width="100%",
                        color="black"
                    ),
                    rx.text(CreateFolderState.error_message, color="red"),
                    rx.button(
                        "Select Mindmaps",
                        on_click=CreateFolderState.toggle_mindmap_list
                    ),
                    # rx.cond(
                    #     CreateFolderState.show_mindmap_list,
                    #     rx.vstack(
                    #         rx.foreach(
                    #             CreateFolderState.available_mindmaps,
                    #             lambda m: rx.hstack(
                    #                 rx.checkbox(
                    #                     is_checked=CreateFolderState.is_mindmap_selected(m["mindmap_id"]),
                    #                     on_change=lambda: CreateFolderState.toggle_mindmap_selection(m["mindmap_id"])
                    #                 ),
                    #                 rx.text(f"{m['mindmap_name']} ({m['terms']} terms)")
                    #             )
                    #         ),
                    #         padding="1em",
                    #         background="white",
                    #         border_radius="md",
                    #         width="100%"
                    #     )
                    # ),
                    rx.button(
                        "Create Folder",
                        on_click=CreateFolderState.submit_folder,
                        # is_disabled=len(CreateFolderState.folder_name) == 0
                    ),
                    spacing="4",
                    padding="20px",
                    align_items="stretch"
                ),
                background_color="white",
                border_radius="12px",
                box_shadow="0px 4px 12px rgba(0,0,0,0.2)",
                width="400px"
            )
        ),
        rx.grid(
            rx.foreach(
                CreateFolderState.folders,
                lambda folder: rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.image(src="/folder.svg", width="70px", height="60px", margin_top="10px", margin_left="10px"),
                            rx.text(folder["folder_name"], font_size="1.2em", font_weight="bold", color="black", margin_top="20px", margin_left="10px"),
                        ),
                        rx.spacer(),
                    ),
                    padding="16px",
                    background_color="#FDE68A",
                    border_radius="16px",
                    box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                    width="400px",
                    height="170px",
                    margin_top="10px",
                    margin_bottom="10px",
                    cursor="pointer",
                )
            ),
            columns="3",
            spacing="6",
            width="100%"
        )
    )