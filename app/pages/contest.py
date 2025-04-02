import reflex as rx
from datetime import datetime
from typing import List
from app.components import sidebar_view


class Contest(rx.State):
    error_message: str = ""
    contests: list[dict] = []
    user_id: str = "user123"
    sort_option: str = "name_asc"  
    search_query: str = ""
    sort_refresh: bool = False

    # Popup state
    show_popup: bool = False
    selected_description: str = ""
    contest_name: str = ""
    contest_owner: str = ""
    contest_created: str = ""
    contest_days_remaining: str = ""
    contest_mindmaps: int = 0
    contest_participants: int = 0
    search_query: str = ""


    mock_user_data = [
        {
            "user_id": "user123",
            "username": "Aroj",
            "email": "aroj@gmail.com",
            "password": "12345",
            "bookmark_mindmap": ["m1", "m2", "m3"],
            "achievement_ids": ["a1", "a2"]
        },
    ]

    mock_contests_data = [
        {
            "contest_name": "AI Art Battle",
            "creator_id": "user123",
            "created_date": "2025-03-31",
            "start_date": "2025-03-31",
            "final_date": "2025-04-30",
            "mindmap_ids": ["m1", "m2", "m3"],
            "participant_ids": ["user123", "user567"],
            "description": "This is a creative contest where participants generate AI-powered artwork to compete for prizes."
        },
        {
            "contest_name": "New Contest",
            "creator_id": "user123",
            "created_date": "2025-03-28",
            "start_date": "2025-03-28",
            "final_date": "2025-03-28",
            "mindmap_ids": ["m1", "m2"],
            "participant_ids": ["user123", "user567"],
            "description": "This contest is about solving interesting logic problems in teams. Open for everyone!"
        }
    ]

    @rx.var(cache=True)
    def filtered_and_sorted_contests(self) -> List[dict]:
        contests = self.contests.copy()  # <--- Add this line

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
        elif self.sort_option == "remaining_days_asc":
            contests.sort(key=lambda x: x["days_remaining_num"])
        elif self.sort_option == "remaining_days_desc":
            contests.sort(key=lambda x: x["days_remaining_num"], reverse=True)
        elif self.sort_option == "num_mindmaps_asc":
            contests.sort(key=lambda x: len(x["mindmap_ids"]))
        elif self.sort_option == "num_mindmaps_desc":
            contests.sort(key=lambda x: len(x["mindmap_ids"]), reverse=True)

        return contests

    
    def get_username(self, user_id: str) -> str:
        for user in self.mock_user_data:
            if user["user_id"] == user_id:
                return user["username"]
        return "Unknown"

    def load_library_data(self):
        try:
            today = datetime.today().date()
            self.contests = []

            for c in self.mock_contests_data:
                if c["creator_id"] != self.user_id:
                    continue

                final_date = datetime.strptime(c["final_date"], "%Y-%m-%d").date()
                days_remaining = (final_date - today).days
                creator_name = self.get_username(c["creator_id"])

                self.contests.append({
                    **c,
                    "participant_count": len(c["participant_ids"]),
                    "days_remaining": "less than a day" if days_remaining <= 0 else f"{days_remaining} days",
                    "days_remaining_num": max(days_remaining, 0),
                    "creator_name": creator_name
                })

        except Exception as e:
            self.error_message = f"An error occurred: {str(e)}"

    def open_popup(self, contest: dict):
        self.contest_name = contest["contest_name"]
        self.contest_owner = contest["creator_name"]
        self.selected_description = contest["description"]
        self.contest_days_remaining = contest["days_remaining"] + " remaining"
        self.contest_created = datetime.strptime(contest["created_date"], "%Y-%m-%d").strftime("%-d %B %Y")
        self.contest_mindmaps = len(contest["mindmap_ids"])
        self.contest_participants = len(contest["participant_ids"])
        self.show_popup = True

    def close_popup(self):
        self.show_popup = False

# ---- Search & Filter ----
def search_and_filter() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Search contests...",
            on_change=Contest.set_search_query,
            value=Contest.search_query,
            width="80%",
            height="50px",
            background_color="white",
            color="black",
            margin_top="30px",
            margin_left="10px",
            font_size="1.1em",
            style={"& input::placeholder": {"color": "#919191"}}
        ),
        rx.menu.root(
            rx.menu.trigger(
                rx.button("Sort By", variant="soft", height="50px", width="100px", font_size="1.1em", margin_top="30px"),
            ),
            rx.menu.content(
                rx.menu.item("Name (A-Z)", on_click=lambda: Contest.set_sort_option("name_asc")),
                rx.menu.item("Name (Z-A)", on_click=lambda: Contest.set_sort_option("name_desc")),
                rx.menu.separator(),
                rx.menu.item("Remaining Days (Fewest)", on_click=lambda: Contest.set_sort_option("remaining_days_asc")),
                rx.menu.item("Remaining Days (Most)", on_click=lambda: Contest.set_sort_option("remaining_days_desc")),
                rx.menu.separator(),
                rx.menu.item("Number of Mindmaps (Least)", on_click=lambda: Contest.set_sort_option("num_mindmaps_asc")),
                rx.menu.item("Number of Mindmaps (Most)", on_click=lambda: Contest.set_sort_option("num_mindmaps_desc")),
            )
            
        ),
        width="100%",
        spacing="4",
        margin_bottom="50px"
    )
    
def contest_page():
    return rx.hstack(
        sidebar_view(),
        rx.box(
            rx.hstack(
                rx.heading(
                    "Contests",
                    font_size="64px",
                    font_weight="bold",
                    color="black",
                    margin_left="20px",
                    margin_top="20px"
                ),
                rx.button(
                    "Create",
                    on_click=lambda: rx.redirect("/create_contest"),
                    width="120px",
                    height="60px",
                    font_size="25px",
                    font_weight="bold",
                    border_radius="12px",
                    bg="#FFDA5D",
                    color="black",
                    border="2px solid #D1D5DB",
                    margin_top="10px",
                    margin_right="40px",
                    margin_left="20px",
                    box_shadow="0 2px 4px rgba(0,0,0,0.1)",
                    _hover={"bg": "#FFE68A"}
                )
            ),
            search_and_filter(),
            rx.foreach(
                Contest.filtered_and_sorted_contests,
                lambda contest: rx.hstack(
                    rx.image(
                        src="/mindmap_icon.svg",
                        width="95px",
                        height="95px",
                        margin_right="10px",
                        margin_left="10px",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.box(
                                rx.text(
                                    f"{contest['contest_name']} | by {contest['creator_name']} | {contest['days_remaining']} remaining",
                                    font_weight="bold",
                                    color="black",
                                    font_size="18px",
                                    margin_left="20px"
                                ),
                                align_self="center",
                            ),
                            rx.spacer(),
                            rx.vstack(
                                rx.image(src="/member_icon.svg", width="20px", height="20px"),
                                rx.text(f"{contest['participant_count']}", color="black"),
                                align="center",
                                spacing="4",
                                margin_right="20px"
                            ),
                            width="100%",
                            align="center",

                        ),
                        border="1px solid #ccc",
                        border_radius="10px",
                        padding="15px",
                        margin_bottom="20px",
                        width="85%",
                        background_color="#fff",
                        box_shadow="0 4px 5px rgba(0, 0, 0, 0.1)",
                        on_click=lambda: Contest.open_popup(contest)
                    ),
                    align="start",
                    width="100%",
                    margin_top="10px"
                )
            ),

            # ---- POPUP -----
            rx.dialog.root(
                rx.dialog.trigger(rx.box()),
                rx.dialog.content(
                    # Close Button
                    rx.box(
                        rx.button("X", on_click=Contest.close_popup, 
                                  bg="#FFDA5D", 
                                  border_radius="10px",
                                  border="2px solid #D1D5DB", 
                                  padding="5px 10px",
                                  font_size="20px",
                                  width="40px",
                                  height="40px",
                                  color="black",
                                  font_weight="bold",
                                  position="absolute",
                                  right="20px",
                                  top="20px",
                                  box_shadow="0 2px 4px rgba(0,0,0,0.1)")
                    ),
                    rx.hstack(
                        rx.box(
                            rx.text(Contest.contest_name, font_size="40px", font_weight="bold", color="black"),
                            rx.text(Contest.selected_description, margin_top="10px", color="black"),
                            margin_right="20px",
                            width="50%"
                        ),
                        rx.box(
                            rx.hstack(
                                rx.text(f"by {Contest.contest_owner}", font_weight="medium", color="black"),
                                rx.text("|", color="black"),
                                rx.text(Contest.contest_days_remaining, font_weight="medium", color="black"),
                                spacing="4"
                            ),
                            rx.divider(margin_y="10px"),
                            rx.text(f"Created on {Contest.contest_created}", color="black"),
                            rx.divider(margin_y="10px"),
                            rx.text(f"{Contest.contest_mindmaps} Mindmaps", color="black"),
                            rx.divider(margin_y="10px"),
                            width="50%",
                            margin_top="50px",
                        ),
                        spacing="4",
                        align="start",
                    ),
                    rx.hstack(
                        rx.button("Join", 
                                  bg="#FFDA5D", 
                                  color="black",
                                  font_size="20px",
                                  border="2px solid #9A9A9A",
                                  width="170px", 
                                  height="40px",
                                  padding_x="32px", 
                                  padding_y="12px", 
                                  font_weight="bold", 
                                  border_radius="12px",
                                 _hover={"bg": "#FFE68A"},
                                 box_shadow="0 2px 2px rgba(0,0,0,0.1)"),                    
                        rx.hstack(
                            rx.image(src="/member_icon.svg", width="20px", height="20px"),
                            rx.text(f"{Contest.contest_participants} joined", color="black"),
                            spacing="2",
                            align="center",
                            margin_top="10px"
                        ),
                        margin_top="40px",
                        spacing="6"
                    ),
                    bg="#fefce8",
                    padding="40px",
                    border_radius="20px",
                    width="800px",
                    min_height="300px",
                    box_shadow="0 4px 12px rgba(0, 0, 0, 0.15)",
                    position="relative"
                ),
                open=Contest.show_popup
            ),

            bg="#FCF8E3",
            width="100%",
            background_color="#fffbe6",
            padding="40px",
            height="100vh",
            overflow_y="auto",
            flex="1"
        ),
        align="start",
        spacing="0",
        on_mount=Contest.load_library_data
    )