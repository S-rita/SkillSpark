import reflex as rx
from typing import List, Dict
from app.components import SidebarToggle, sidebar, sidebar_expand


class State(rx.State):
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
            "description": "Get 100% on a mindmap"
        },
        {
            "id": "chicken_dinner", 
            "name": "Chicken dinner",
            "image": "/Chicken_dinner.png",
            "category": "best",
            "completion": True,
            "description": "Win first place in a contest"
        },
        {
            "id": "one_take_wonder",
            "name": "One-Take Wonder", 
            "image": "/One_take_Wonder.png",
            "category": "best",
            "completion": True,
            "description": "Complete a mindmap perfectly on first try"
        },

        # One step ahead achievements
        {
            "id": "mind_mapper",
            "name": "Mind Mapper",
            "image": "/Mind_Mapper.png", 
            "category": "neutral",
            "completion": False,
            "description": "Create your first mindmap"
        },
        {
            "id": "brave_entry",
            "name": "Brave Entry",
            "image": "/Brave_Entry.png",
            "category": "neutral", 
            "completion": True,
            "description": "Enter your first contest"
        },
        {
            "id": "creative_flow",
            "name": "Creative Flow",
            "image": "/Creative_Flow.png",
            "category": "neutral",
            "completion": False,
            "description": "Create 5 mindmaps"
        },
        {
            "id": "first_step",
            "name": "First Step",
            "image": "/First_Step.png",
            "category": "neutral",
            "completion": True,
            "description": "Complete your first mindmap"
        },
        {
            "id": "back_on_track",
            "name": "Back on Track",
            "image": "/Back_on_Track.png",
            "category": "neutral",
            "completion": True,
            "description": "Resume learning after a break"
        },

        # Best of the worst achievements
        {
            "id": "epic_oops",
            "name": "Epic Oops",
            "image": "/Epic_Oops.png",
            "category": "worst",
            "completion": False,
            "description": "Get 0% on a mindmap"
        },
        {
            "id": "better_luck",
            "name": "Better Luck Next Time",
            "image": "/Better_Luck_Next_Time.png",
            "category": "worst",
            "completion": False,
            "description": "Fail a contest"
        },

        # Daily streak achievements
        {
            "id": "triple_flame",
            "name": "Triple Flame",
            "image": "/Triple_Flame.png",
            "category": "daily",
            "completion": False,
            "description": "3 day streak"
        },
        {
            "id": "high_five",
            "name": "High Five Hustler",
            "image": "/High_Five_Hustler.png",
            "category": "daily",
            "completion": False,
            "description": "5 day streak"
        },
        {
            "id": "tenacious",
            "name": "Tenacious Ten",
            "image": "/Tenacious_Ten.png",
            "category": "daily",
            "completion": False,
            "description": "10 day streak"
        },
        {
            "id": "power_twenty",
            "name": "Power of Twenty",
            "image": "/Power_of_Twenty.png",
            "category": "daily",
            "completion": False,
            "description": "20 day streak"
        },
        {
            "id": "thirty_titan",
            "name": "Thirty Day Titan",
            "image": "/Thirty_Day_Titan.png",
            "category": "daily",
            "completion": True,
            "description": "30 day streak"
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

def achievement_circle(achievement: dict) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.image(
                src=achievement["image"],
                width="70%",
                height="70%",
                object_fit="contain",
            ),
            width="150px",
            height="150px", 
            border_radius="50%",
            overflow="hidden",
            bg="#F5F5F5",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
            display="flex",
            justify_content="center",
            align_items="center",
            background_color="#FFFFFF",
            # Only add filter if achievement is not completed
            # Use rx.cond for conditional rendering
            filter=rx.cond(
                achievement["completion"] == False,
                "brightness(0.5)",
                "",
            ),
            
        ),
        rx.text(
            achievement["name"],
            font_size="1em",
            color="white",
            margin_top="0.5em",
        ),
        width="100%",
        align_items="center",
    )

def Top_area() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Achievements", 
            font_size="2em", 
            font_weight="bold", 
            width="50%",
            align="left",
            color="black",
            margin_bottom="0.5em",  # Add space between text and box
        ),
        rx.box(
            rx.image(
                src=State.level_image,  # Replace with your image path
                width="100%",
                height="100%",
                object_fit="contain",
                style={"& img": {"object_fit": "contain"}},
                
            ),
            background_color="#1E1E1E",
            width="50%",  # Takes up 90% of the parent container width
            height="25vh",  # Set a fixed height
            border_radius="1.5em",  # Curved borders
            overflow="hidden",  # Ensures content stays within border radius
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
        ),
        
        rx.text(
            f"Level: {State.user_level}", 
            font_size="1.5em", 
            font_weight="bold", 
            width="50%",
            align="left",
            color="#4F4F4F",
            margin_top="1em",  # Add space between text and box
        ),
        rx.text(
            f"Completed Tasks: {State.completed_count}/15", 
            font_size="1em", 
            font_weight="bold", 
            width="50%",
            align="left",
            color="#ABABAB",
            margin_bottom="1em",  # Add space between text and box
        ),
        rx.box(  # Add horizontal line
            width="60%",  # Match the width of the image box above
            height="2px",  # Line thickness
            bg="#ABABAB",  # Line color matching text color
            margin_top="0",
            align_self="start",
        ),
        width="100%",
        align_items="left",  # Centers children horizontally
        spacing="0",  # Adds consistent spacing between elements
        margin_left="3em",
    )


# def goodAchievements() -> rx.Component:
    return rx.vstack(
        # Title
        rx.text(
            "Best of the best",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        # Main container box
        rx.box(
            # Horizontal stack for the three circles
            rx.hstack(
                # First circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Perfectionist.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                            # filter="brightness(0.7)",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",
                    ),
                    rx.text(
                        "Perfectionist",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Second circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Chicken_dinner.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                    ),
                    rx.text(
                        "Chicken dinner",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Third circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/One_take_Wonder.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",
                    ),
                    rx.text(
                        "One-Take Wonder",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                spacing="9",  # Space between circles
                width="100%",
                
                padding="5em 10em 5em 6em",  # Padding around the circles
            ),
            width="80vw",  # Box takes up 90% of screen width
            border_radius="1em",  # Curved borders
            bg="#ABABAB", 
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",  # Box takes up 90% of screen width
        align_items="left",  # Centers children horizontally
        margin_left="5em",  # Centers children horizontally

    )

def goodAchievements() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Best of the best",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        rx.box(
            rx.grid(
                rx.foreach(
                    State.best_achievements,
                    achievement_circle,
                ),
                columns="4",
                spacing="9",
                width="100%",
                padding="5em 10em 5em 6em",
            ),
            width="100%",
            border_radius="1em",
            bg="#ABABAB",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",
        align_items="left",
        margin_left="2em",
        margin_bottom="2em",  # Add space between text and box
    )


def neutralAchievements() -> rx.Component:
    return rx.vstack(
        rx.text(
            "One step ahead",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        rx.box(
            rx.grid(
                rx.foreach(
                    State.neutral_achievements,
                    achievement_circle
                ),
                columns="4",  # Set 2 columns
                spacing="9",
                width="100%",
                padding="5em 10em 5em 6em",
            ),
            width="100%",
            border_radius="1em",
            bg="#ABABAB",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",
        align_items="left",
        margin_left="2em",
        margin_bottom="2em",  # Add space between text and box
    )

# def neutralAchievements() -> rx.Component:
    return rx.vstack(
        # Title
        rx.text(
            "One step ahead",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        # Main container box
        rx.box(
            # Horizontal stack for the three circles
            rx.hstack(
                # First circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Mind_Mapper.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "Mind Mapper",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Second circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Brave_Entry.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "Brave Entry",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Third circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Creative_Flow.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "Creative Flow",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Fourth circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/First_Step.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "First Step",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Fifth circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Back_on_Track.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                    ),
                    rx.text(
                        "Back on Track",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                spacing="9",  # Space between circles
                width="100%",
                padding="5em 10em 5em 6em",  # Padding around the circles
            ),
            width="80vw",  # Box takes up 90% of screen width
            border_radius="1em",  # Curved borders
            bg="#ABABAB",  # Light background
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",  # Box takes up 90% of screen width
        align_items="left",  # Centers children horizontally
        margin_left="5em",  # Centers children horizontally
        margin_top="2em",  # Add space between text and box
    )

def badAchievements() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Best of the worst",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        rx.box(
            rx.grid(
                rx.foreach(
                    State.worst_achievements,
                    achievement_circle
                ),
                columns="4",
                spacing="9",
                width="100%",
                padding="5em 10em 5em 6em",
            ),
            width="100%",
            border_radius="1em",
            bg="#ABABAB",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",
        align_items="left",
        margin_left="2em",
        margin_bottom="2em",  # Add space between text and box

    )

# def badAchievements() -> rx.Component:
    return rx.vstack(
        # Title
        rx.text(
            "Best of the worst",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        # Main container box
        rx.box(
            # Horizontal stack for the three circles
            rx.hstack(
                # First circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Epic_Oops.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                            # filter="brightness(0.7)",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",
                    ),
                    rx.text(
                        "Epic Oops",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Second circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Better_Luck_Next_Time.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",
                    ),
                    rx.text(
                        "Better Luck Next Time",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                spacing="9",  # Space between circles
                width="100%",
                
                padding="5em 10em 5em 6em",  # Padding around the circles
            ),
            width="80vw",  # Box takes up 90% of screen width
            border_radius="1em",  # Curved borders
            bg="#ABABAB", 
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",  # Box takes up 90% of screen width
        align_items="left",  # Centers children horizontally
        margin_left="5em",  # Centers children horizontally
        margin_top="2em",  # Add space between text and box
    )


def dailyAchievements() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Daily streaks",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        rx.box(
            rx.grid(
                rx.foreach(
                    State.daily_achievements,
                    achievement_circle
                ),
                columns="4",
                spacing="9",
                width="100%",
                padding="5em 10em 5em 6em",
            ),
            width="100%",
            border_radius="1em",
            bg="#ABABAB",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",
        align_items="left",
        margin_left="2em",
        margin_bottom="2em",  # Add space between text and box
    )


# def dailyAchievements() -> rx.Component:
    return rx.vstack(
        # Title
        rx.text(
            "Daily streaks",
            font_size="2em",
            font_weight="bold",
            color="#4F4F4F",
            margin_bottom="0",
        ),
        # Main container box
        rx.box(
            # Horizontal stack for the three circles
            rx.hstack(
                # First circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Triple_Flame.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "Triple Flame",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Second circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/High_Five_Hustler.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "High Five Hustler",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Third circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Tenacious_Ten.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "Tenacious Ten",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Fourth circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Power_of_Twenty.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                        filter="brightness(0.5)",

                    ),
                    rx.text(
                        "Power of Twenty",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                # Fifth circle
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/Thirty_Day_Titan.png",
                            width="70%",
                            height="70%",
                            object_fit="contain",
                        ),
                        width="150px",  # Set fixed width for circle
                        height="150px",  # Set fixed height equal to width for perfect circle
                        border_radius="50%",  # Makes the box circular
                        overflow="hidden",  # Ensures image stays within circular border
                        bg="#F5F5F5",  # Optional: background color
                        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",  # Optional: adds depth
                        display="flex",  # Enable flexbox
                        justify_content="center",  # Center horizontally 
                        align_items="center",  # Center vertically
                        background_color="#FFFFFF",  # Light background
                    ),
                    rx.text(
                        "Thirty Day Titan",
                        font_size="1em",
                        color="white",
                        margin_top="0.5em",
                    ),
                    align_items="center",
                ),
                spacing="9",  # Space between circles
                width="100%",
                padding="5em 10em 5em 6em",  # Padding around the circles
            ),
            width="80vw",  # Box takes up 90% of screen width
            border_radius="1em",  # Curved borders
            bg="#ABABAB",  # Light background
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.1)",
        ),
        width="100%",  # Box takes up 90% of screen width
        align_items="left",  # Centers children horizontally
        margin_left="5em",  # Centers children horizontally
        margin_top="2em",  # Add space between text and box
    )






def Main_content() -> rx.Component:
    return rx.vstack(
        goodAchievements(),
        neutralAchievements(),
        badAchievements(),
        dailyAchievements(),
        spacing="2",
        width="100%",
    )



def layout(*children):
    return rx.hstack(
        rx.cond(
            SidebarToggle.expanded,
            sidebar_expand(),
            sidebar(),
        ),
        rx.box(
            *children,
            flex="1",  # Takes up remaining space
            height="100vh",
            overflow_y="auto",
        ),
        width="100%",
        spacing="0",
    )

def Achievements_page() -> rx.Component:
    return layout( 
        rx.vstack(
            Top_area(),
            Main_content(),
            spacing="9",
            background_color="#FFFBEA",
            width="100%",
            height="100%",
            overflow_y="auto",  
            overflow_x="auto", 
            padding="4em 4em 4em 4em",
        )
    )