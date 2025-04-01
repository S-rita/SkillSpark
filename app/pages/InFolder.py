
# from app.states import CreateFolderState

# @rx.page(route="/folder/[folder_name]")
# async def folder_page(folder_name: str) -> rx.Component:
#     await CreateFolderState.load_folders()

#     folder = next((f for f in CreateFolderState.folders if f["folder_name"] == folder_name), None)

#     if not folder:
#         return rx.text("Folder not found.", color="red")

#     mindmaps_in_folder = [
#         m for m in CreateFolderState.available_mindmaps
#         if m["mindmap_id"] in folder["mindmap_ids"]
#     ]

#     return rx.vstack(
#         rx.heading(f"📁 {folder['folder_name']}"),
#         rx.text(f"{len(mindmaps_in_folder)} mindmaps:"),
#         rx.vstack(
#             rx.foreach(
#                 mindmaps_in_folder,
#                 lambda m: rx.text(f"{m['mindmap_name']} ({m['terms']} terms)")
#             )
#         ),
#         padding="2em"
#     )

import reflex as rx
from typing import List
from app.components import sidebar_view

class FolderState(rx.State):
    user: str = "user123"
    sort_option: str = "name_asc"  
    search_query: str = ""
    sort_refresh: bool = False

    selected_folder: dict = {
        "folder_name": "Testing Folder",
        "owner_id": "user123",
        "mindmap_ids": ["m1", "m2", "m3"]
    }

    available_mindmaps: List[dict] = [
        {"mindmap_id": "m1", "mindmap_name": "Python Basics", "created_date": "2024-01-10", "creator_id": "user123", "accessibility": True, "terms": 10},
        {"mindmap_id": "m2", "mindmap_name": "Data Structures", "created_date": "2024-02-05", "creator_id": "user123", "accessibility": True, "terms": 20},
        {"mindmap_id": "m3", "mindmap_name": "React Concepts", "created_date": "2024-03-15", "creator_id": "user456", "accessibility": True, "terms": 40},
    ]

    @rx.var
    def mindmaps_in_folder(self) -> List[dict]:
        mindmap_ids = self.selected_folder["mindmap_ids"]
        mindmaps = [m for m in self.available_mindmaps if m["mindmap_id"] in mindmap_ids]

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
        

# ---- Search & Filter ----
def search_and_filter() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Search mindmaps...",
            on_change=FolderState.set_search_query,
            value=FolderState.search_query,
            width="80%",
            height="50px",
            background_color="white",
            color="black",
            font_size="1.1em",
            style={"& input::placeholder": {"color": "#919191"}},
            margin_left="10px"
        ),
        rx.menu.root(
            rx.menu.trigger(
                rx.button("Sort By", variant="soft", height="50px", width="100px", font_size="1.1em"),
            ),
            rx.menu.content(
                rx.menu.item("Name (A-Z)", on_click=lambda: FolderState.set_sort_option("name_asc")),
                rx.menu.item("Name (Z-A)", on_click=lambda: FolderState.set_sort_option("name_desc")),
                rx.menu.separator(),
                rx.menu.item("Date (Oldest First)", on_click=lambda: FolderState.set_sort_option("date_asc")),
                rx.menu.item("Date (Newest First)", on_click=lambda: FolderState.set_sort_option("date_desc")),
                rx.menu.separator(),
                rx.menu.item("Number of Terms (Least)", on_click=lambda: FolderState.set_sort_option("num_terms_asc")),
                rx.menu.item("Number of Terms (Most)", on_click=lambda: FolderState.set_sort_option("num_terms_desc")),
            )
        ),
        width="100%",
        spacing="4",
    )
  
def folder_page() -> rx.Component:
    return rx.hstack(
        sidebar_view(),
        rx.box(
            rx.heading(FolderState.selected_folder["folder_name"], color="black", margin_bottom="40px", font_size="50px", margin_top="20px"),
            search_and_filter(), 
            rx.grid(
                rx.foreach(
                    FolderState.mindmaps_in_folder,
                    lambda m: rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.image(src="/tree.svg", width="70px", height="60px", margin_top="10px", margin_left="10px"),
                                rx.text(m["mindmap_name"], font_size="1.2em", font_weight="bold", color="black", margin_top="20px", margin_left="10px"),
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
                        margin_top="40px",
                        cursor="pointer",
                        margin_bottom="10px",
                    )
                ),
                columns="3",
                spacing="6",
                width="100%",
            ),
            background_color="#fffbe6",
            padding="40px",
            height="100vh",
            overflow_y="auto",
            flex="1",
        ),
        align="start",
        spacing="0",
        width="100%",
    )