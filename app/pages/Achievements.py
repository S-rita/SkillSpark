import reflex as rx
from app.components import SidebarToggle, sidebar, sidebar_expand
from app.states import Achiecement_State




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
                src=Achiecement_State.level_image,  # Replace with your image path
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
            f"Level: {Achiecement_State.user_level}", 
            font_size="1.5em", 
            font_weight="bold", 
            width="50%",
            align="left",
            color="#4F4F4F",
            margin_top="1em",  # Add space between text and box
        ),
        rx.text(
            f"Completed Tasks: {Achiecement_State.completed_count}/15", 
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
                    Achiecement_State.best_achievements,
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
                    Achiecement_State.neutral_achievements,
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
                    Achiecement_State.worst_achievements,
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
                    Achiecement_State.daily_achievements,
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