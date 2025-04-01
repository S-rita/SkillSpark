import reflex as rx
from typing import List
from app.components import sidebar_view
from datetime import datetime, date
import httpx
from app.states import Library, CreateFolderState

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
        sidebar_view(), 

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
                        rx.image(src="/tree.svg", width="70px", height="60px", margin_top="10px", margin_left="10px"),
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
                            src="/tree.svg",
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

def mindmap_item(m):
    return rx.hstack(
        rx.checkbox(
            is_checked=CreateFolderState.is_selected(m),
            on_change=lambda checked: CreateFolderState.toggle_mindmap_selection_by_id(m["mindmap_id"]),
        ),
        rx.text(f"{m['mindmap_name']} ({m['terms']} terms)", color="black"),
    )
   
# ---- Folder View ---- 
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
                    rx.cond(
                        CreateFolderState.show_mindmap_list,
                        rx.vstack(
                                rx.foreach(
                                CreateFolderState.available_mindmaps,
                                lambda m: rx.box(
                                    mindmap_item(m),
                                    margin_top="1em",
                                    margin_bottom="1em" 
                                ),
                            ),
                            padding="1em",
                            background="white",
                            border_radius="md",
                            width="100%"
                        )
                    ),
                    rx.button(
                        "Create Folder",
                        on_click=CreateFolderState.create_folder,
                    ),
                    spacing="4",
                    padding="20px",
                    align_items="stretch",
                ),
                background_color="white",
                border_radius="12px",
                box_shadow="0px 4px 12px rgba(0,0,0,0.2)",
                width="400px",
            )
        ),
        rx.grid(
            rx.foreach(
    CreateFolderState.folders,
    lambda folder: rx.link(
        rx.box(
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
        ),
        # href=f"/folder/{folder['folder_name']}"
    )
),
            columns="3",
            spacing="6",
            width="100%"
        )
    )