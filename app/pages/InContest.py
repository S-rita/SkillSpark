import reflex as rx
from app.components import sidebar_view
from typing import List

class InContest(rx.State):
    user: str = "user123"

    available_mindmaps: List[dict] = [
        {"mindmap_id": "m1", "mindmap_name": "Python Basics", "created_date": "2024-01-10", "creator_id": "user123", "accessibility": True, "terms": 10},
        {"mindmap_id": "m2", "mindmap_name": "Data Structures", "created_date": "2024-02-05", "creator_id": "user123", "accessibility": True, "terms": 20},
        {"mindmap_id": "m3", "mindmap_name": "React Concepts", "created_date": "2024-03-15", "creator_id": "user456", "accessibility": True, "terms": 40},
    ]
    
    mock_user_data = [
        {
            "user_id": "user123",
            "username": "Aroj",
            "email": "aroj@gmail.com",
            "password": "12345",
            "bookmark_mindmap": ["m1", "m2", "m3"],
            "achievement_ids": ["a1", "a2"]
        },
        {
            "user_id": "user456",
            "username": "Jaja",
            "email": "jaja@gmail.com",
            "password": "12345",
            "bookmark_mindmap": ["m1", "m2"],
            "achievement_ids": ["a1", "a2"]
        },
    ]

    mock_contests_data: dict = {
        "contest_name": "AI Art Battle",
        "creator_id": "user123",
        "created_date": "2025-03-31",
        "start_date": "2025-03-31",
        "final_date": "2025-04-30",
        "mindmap_ids": ["m1", "m2", "m3"],
        "participant_ids": ["user123", "user456"],
    "description": "This is an exciting and creative contest where participants are challenged to generate original, AI-powered artwork using cutting-edge technology. Whether you're an experienced digital artist or just exploring the world of artificial intelligence, this competition invites you to showcase your imagination, innovation, and artistic flair."
    }

    @rx.var
    def contest_name(self) -> str:
        return self.mock_contests_data["contest_name"]

    @rx.var
    def selected_description(self) -> str:
        return self.mock_contests_data["description"]

    @rx.var
    def contest_owner(self) -> str:
        creator_id = self.mock_contests_data["creator_id"]
        user = next((u for u in self.mock_user_data if u["user_id"] == creator_id), {})
        return user.get("username", "Unknown")

    @rx.var
    def contest_days_remaining(self) -> str:
        from datetime import datetime
        final = datetime.strptime(self.mock_contests_data["final_date"], "%Y-%m-%d")
        now = datetime.now()
        days_remaining = (final - now).days
        return f"{days_remaining} days left" if days_remaining > 0 else "Expired"

    @rx.var
    def contest_created(self) -> str:
        return self.mock_contests_data["created_date"]

    @rx.var
    def contest_mindmaps(self) -> int:
        return len(self.mock_contests_data["mindmap_ids"])

    @rx.var
    def contest_participants(self) -> int:
        return len(self.mock_contests_data["participant_ids"])

def inContest_page():
    return rx.hstack( 
        sidebar_view(), 
        rx.box( 
            rx.box(
                rx.button("X", 
                          bg="#FFDA5D", 
                          border_radius="10px",
                          border="2px solid #D1D5DB", 
                          padding="5px 10px",
                          font_size="30px",
                          width="50px",
                          height="50px",
                          color="black",
                          font_weight="bold",
                          position="absolute",
                          right="20px",
                          top="20px",
                          box_shadow="0 2px 4px rgba(0,0,0,0.1)"),
                          on_click=rx.redirect("/contest")
            ),
            rx.hstack(
                rx.box(
                    rx.text(InContest.contest_name, font_size="40px", font_weight="bold", color="black"),
                    rx.text(InContest.selected_description, margin_top="10px", color="black"),
                    margin_right="20px",
                    width="50%"
                ),
                rx.box(
                    rx.hstack(
                        rx.text(f"by {InContest.contest_owner}", font_weight="medium", color="black"),
                        rx.text("|", color="black"),
                        rx.text(InContest.contest_days_remaining, font_weight="medium", color="black"),
                        spacing="4",
                        margin_top="20px"
                    ),
                    rx.divider(margin_y="10px"),
                    rx.text(f"Created on {InContest.contest_created}", color="black"),
                    rx.divider(margin_y="10px"),
                    width="50%",
                    margin_top="50px",
                ),
                spacing="4",
                align="start",
            ),

            # 👉 New stat boxes added here
            rx.hstack(
                rx.box(
                    rx.hstack(
                        rx.image(src="/yellow_tree.svg", width="50px", height="50px"),
                        rx.box(
                            rx.text(InContest.contest_mindmaps, font_size="28px", color="white", font_weight="bold", margin_top="-5px"),
                            rx.text("Mind Maps", color="white", font_size="14px"),
                        ),
                        spacing="4",
                        align="center",
                    ),
                    bg="#2B292B",
                    padding="20px",
                    border_radius="10px",
                    width="220px",
                    height="100px"
                ),
                rx.box(
                    rx.hstack(
                        rx.image(src="/yellow_user.svg", width="40px", height="40px"),
                        rx.box(
                            rx.text(InContest.contest_participants, font_size="28px", color="white", font_weight="bold", margin_top="-5px"),
                            rx.text("Participants", color="white", font_size="14px"),
                            spacing="0"
                        ),
                        spacing="4",
                        align="center"
                    ),
                    bg="#2B292B",
                    padding="20px",
                    border_radius="10px",
                    width="220px",
                    height="100px"
                ),
                spacing="8",
                margin_top="40px"
            ),

            rx.vstack(
                rx.text("Mind Maps", font_size="24px", font_weight="bold", margin_bottom="5px", color="black", margin_left="10px"),
                rx.foreach(
                    InContest.available_mindmaps,
                    lambda mindmap: rx.hstack(
                        rx.box(
                            rx.text(mindmap["mindmap_name"], font_size="18px", color="black", font_weight="medium"),
                            rx.text(f'{mindmap["terms"]} terms', font_size="14px", color="gray"),
                            spacing="1"
                        ),
                        rx.spacer(),
                        rx.button("Start", 
                            bg="#FFDA5D", 
                            color="black",
                            border="2px solid #9A9A9A",
                            border_radius="10px",
                            padding_x="16px",
                            height="40px",
                            width="100px",
                            padding_y="6px",
                            font_size="20px",
                            font_weight="bold",
                            _hover={"bg": "#FFE68A"},
                            box_shadow="0 2px 2px rgba(0,0,0,0.1)"
                        ),
                        width="100%",
                        padding="12px",
                        bg="white",
                        border_radius="12px",
                        box_shadow="0 2px 4px rgba(0,0,0,0.05)",
                        align="center"
                    )
                ),
                spacing="4",
                margin_top="40px",
                width="100%"
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
