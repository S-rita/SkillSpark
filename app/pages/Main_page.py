import reflex as rx
from app.components import SidebarToggle, sidebar, sidebar_expand
from app.states import Main_Pages_state

def search_area() -> rx.Component:
    return rx.hstack(
        rx.input(
            rx.input.slot(
                rx.image(
                    src="/searchArea.png",
                    width="100%",
                    height="90%",
                    fit='cover',
                    padding="0.5em",
                ),
            ),
            value=Main_Pages_state.search_text,  # Bind value to state
            on_change=Main_Pages_state.set_search,  # Update state when input changes
            placeholder="Search public mindmaps and contests",
            width="65vw",
            height="100px",
            bg='white',
            outline="none",
            style={
                "& input::placeholder": {"color": "grey", "opacity": "0.25"},
            },
            border_radius="0.5em",
            color="grey",
            font_size="2em",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.25)",
        ),
        rx.button(
            "Search",
            on_click=Main_Pages_state.handle_search,  # Add click handler
            color="black",
            font_size="2em",
            font_weight="bold",
            bg="#FFDA5D",
            border_radius="8px",
            padding="10px",
            width="6em",
            height="60px",
            overflow="hidden",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
            _hover={
                "transform": "scale(1.05)",
                "transition": "transform 0.2s ease-in-out",
                "cursor": "pointer",
            }
        ),
        align="center",
        justify_content="space-between",
        width="100%",
    )



def recent_mindmap_item(mindmap: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.image(
                    src=mindmap["image"],
                    width="100%",
                    height="100%",
                    object_fit="cover"
                ),
                bg="#FFDA5D",
                border_radius="1.5em",
                padding="1em",
                width="6em",
                height="6em",
                overflow="hidden",
                box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                }
            ),
            rx.vstack(
                rx.text(mindmap["name"], font_size="2em", font_weight="bold", color="black"),
                rx.text(
                    f"Mindmap set    ●    {mindmap['terms']} terms    ●    by {mindmap['creator']}", 
                    font_size="1em",
                    color="#969696",
                    margin_left="1em",
                    white_space="pre",
                ),
                spacing="0",
                align_items="start",
            ),
            align="center",
            spacing="6",
            _hover={
                    "transform": "scale(1.02)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                }
        ),
        margin_right="6em",
        width="100%",  # Full width for the box
    )

def recent_mindmaps_section() -> rx.Component:
    return rx.vstack(
        rx.text("Recents", font_size="4em", font_weight="bold", color="black", align="left",width="100%"),
        rx.grid(  # Use grid instead of vstack for the items
            rx.foreach(
                Main_Pages_state.recent_mindmaps,
                recent_mindmap_item
            ),
            columns="2",  # Set 2 columns
            spacing="6",  # Add spacing between grid items
            width="100%",
        ),
        spacing="4",
        padding="0 4em 4em 4em",  # Add padding inside the background
        width="100%",  # Make hstack take full width
        align_self="left",
    )



def favorite_mindmap_item(mindmap: rx.Var) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(mindmap["name"], font_size="1.5em", font_weight="bold", color="black"),
            rx.box(
                f"{mindmap["terms"]} terms",
                font_size="0.75em",
                color="black",
                background_color="#FFF5D0",
                border_radius="1.5em",
                padding="1px 20px 1px 20px",
                width="fit-content",
                height="fit-content",
                margin_bottom="2em",
            ),
            rx.hstack(
                rx.avatar(
                    src=mindmap["image"].to_string(),
                    size="3",
                    radius="full",
                    fallback="",
                    variant="solid",
                    color_scheme="gray",
                    opacity="1",
                    high_contrast=False,
                ),
                rx.text(mindmap["creator"], font_size="1em", color="black"),
                spacing="2",
                align_items="center",
                justify_content="center",
                margin_top="2em",
            ),
        ),
        background_color="#FFDA5D",
        border_radius="1rem",
        width="33%",
        overflow="hidden",
        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
        _hover={
            "transform": "scale(1.05)",
            "transition": "transform 0.2s ease-in-out",
            "cursor": "pointer",
        },
        padding="2em 1.5em 2em 1.5em",
    )



def creator_item(creator: rx.Var, index: rx.Var) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.avatar(
                    src=creator["image"].to_string(),
                    size="6",
                    radius="full",
                    fallback="",
                    variant="solid",
                    color_scheme="gray",
                    opacity="1",
                    high_contrast=False,
                    margin_bottom="2em",
                ),
                rx.text(creator["name"], font_size="1.5em", font_weight="bold", color="black"),
                spacing="2",
                align_items="center",
                justify_content="center",
            ),
            
            rx.hstack(
                rx.box(
                    rx.hstack(
                        rx.image(
                            src="/smallM.png",
                            width="20px",
                            height="20px",
                            fit='cover',
                        ),
                        rx.text(
                            f"{creator['mindmap_count'].to_string()} mindmap sets",
                            font_size="0.75em",
                            color="black",
                        ),
                        align="center",
                        spacing="1",
                    ),
                    background_color="#FFF5D0",
                    border_radius="1em",
                    padding="1px 5px",
                    width="fit-content",
                    height="fit-content",
                ),
                rx.box(
                    rx.hstack(
                        rx.image(
                            src="/champ.png",
                            width="20px",
                            height="20px",
                            fit='cover',
                        ),
                        rx.text(
                            f"{creator['contest_count'].to_string()} contests",
                            font_size="0.75em",
                            color="black",
                        ),
                        align="center",
                        spacing="1",
                    ),
                    background_color="#FFF5D0",
                    border_radius="1em",
                    padding="1px 5px",
                    width="fit-content",
                    height="fit-content",
                ),
                spacing="2",
            ),
            position="relative",
            z_index="2"
        ),
        position="relative",
        _before={
            "content": "''",
            "position": "absolute",
            "top": "1em",
            "right": "2em",
            "width": "60%",  # Match the background_size you had
            "height": "60%",
            "background_size": "contain",
            "background_position": "right center",
            "background_repeat": "no-repeat",
            "background_image": rx.cond(  # Use rx.cond for conditional rendering
                index == 0,
                "url('/rank1.png')",
                rx.cond(
                    index == 1,
                    "url('/rank2.png')",
                    "url('/rank3.png')"
                )
            ),
            "opacity": "1",  # Adjust this value to control opacity (0.0 to 1.0)
            "z_index": "1",
            "backdrop_filter": "drop-shadow(100px 100px 100px black)",
        },
        background_color="#FFDA5D",
        border_radius="1rem",
        width="33%",
        overflow="hidden",
        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
        _hover={
            "transform": "scale(1.05)",
            "transition": "transform 0.2s ease-in-out",
            "cursor": "pointer",
        },
        padding="2em 1.5em 2em 1.5em",
        align="start",
        
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
            width=rx.cond(
                SidebarToggle.expanded,
                "calc(100vw - 300px)",
                "calc(100vw - 100px)"
            ),
        ),
        width="100%",
        spacing="0",
        overflow="hidden",
    )

# Your favorite mindmaps section
def favorites_section():
    return rx.vstack(
        rx.hstack(
            rx.text("Favorites", font_size="4em", font_weight="bold", color="black", align="left"),
            rx.link(
                rx.text(
                    "View all",
                    color="#CAC7BA",
                    font_size="1.5em",
                    font_weight="bold", 
                    _hover={
                    "text_decoration": "none",
                    "color": "#919191",
                    "transition": "color 0.2s ease-in-out"
                    },
                ),
                href="/egg",
                _hover={
                    "text_decoration": "none",
                },
                style={
                    "transition": "color 0.3s ease-in-out"  # Add transition to base style
                }
            ),
            width="100%",
            align="baseline",
            justify_content="space-between",
        ),
        rx.hstack(
            rx.cond(
                Main_Pages_state.can_go_prev,
                rx.button(
                    rx.icon("chevron-left"),
                    on_click=Main_Pages_state.prev_slide,
                    variant="surface",
                    color_scheme="gray",
                    color="#848A95",
                    background="white",  # Add white background
                    border="1px solid #E2E8F0",  # Add border
                    border_radius="50%",  # Make it circular
                    width="40px",  # Set fixed width
                    height="40px",  # Set fixed height
                    _hover={
                        "background": "white",
                        "color": "#0F2552",
                        "transform": "scale(1.1)",
                        "transition": "all 0.2s ease-in-out",
                        "box_shadow": "0px 3px 5px rgba(0, 0, 0, 0.1)"
                    },
                ),
            ),
            rx.hstack(
                rx.foreach(
                    Main_Pages_state.visible_mindmaps,
                    favorite_mindmap_item
                ),
                spacing="7",
                width="100%",
                justify="start",
                align="start",
            ),
            rx.cond(
                Main_Pages_state.can_go_next,
                rx.button(
                    rx.icon("chevron-right"), 
                    on_click=Main_Pages_state.next_slide,
                    variant="surface",
                    color_scheme="gray",
                    color="#848A95",
                    background="white",  # Add white background
                    border="1px solid #E2E8F0",  # Add border
                    border_radius="50%",  # Make it circular
                    width="40px",  # Set fixed width
                    height="40px",  # Set fixed height
                    _hover={
                        "background": "white",
                        "color": "#0F2552",
                        "transform": "scale(1.1)", 
                        "transition": "all 0.2s ease-in-out",
                        "box_shadow": "0px 5px 3px rgba(0, 0, 0, 0.1)"
                    },
                ),
            ),
            spacing="4",
            width="100%",
            align="center",
        ),
        spacing="4",
        padding="0 4em 4em 4em",
        width="100%",
        align_self="start",
    )

def index_main() -> rx.Component:
    return layout(
            rx.vstack(
            # Top Area
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(f"Hello {Main_Pages_state.current_user['username']}🤫", font_size="6em", font_weight="bold", color="black"),
                        rx.text("Welcome back, let's start practice today", font_size="1.5em", color='#919191'),
                    ),
                    rx.hstack(
                        rx.button(
                            rx.image(src="/AddM.png", width="100%", height="100%",fit='cover',),
                            bg="#FDCC00",
                            width="6em",
                            border_radius="8px",  # Optional: Rounded corners
                            padding="10px",
                            height="6em",
                            overflow="hidden",
                            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                            _hover={
                                "transform": "scale(1.05)",
                                "transition": "transform 0.2s ease-in-out",
                                "cursor": "pointer",
                            }
                        ),
                        # Fixed size avatar
                        rx.box(
                            rx.avatar(
                                src=Main_Pages_state.current_user["image"],
                                size="9",
                                radius="full",
                                fallback="PROFILE",
                                variant="solid",
                                color_scheme="gray",
                                opacity="1",
                                high_contrast=False,
                                background_color="white",
                            ),
                            width="fit-content",
                            height="fit-content",
                        ),
                        align="center",
                        spacing="7",
                        width="auto",  # Full width for the hstack
                    ),

                    spacing="2",
                    align_items="start",
                    width="100%",
                    justify_content="space-between",
                ),
                rx.hstack(
                    search_area(),
                    width="100%",
                ),
                padding="4em 4em 0 4em",  # Add padding inside the background
                width="100%",  # Full width of the viewport
            ),

            recent_mindmaps_section(),


            # Favorites
            favorites_section(),


            # Top Creators
            rx.vstack(
                rx.text("Top Creators", font_size="4em", font_weight="bold", color="black", align="left",width="100%"),
                rx.hstack(
                    rx.foreach(
                        Main_Pages_state.top_creators,
                        lambda creator, index: creator_item(creator, index),
                    ),
                    spacing="7",
                    width="100%",
                    justify="start",
                    align="start",
                ),
                spacing="4",
                margin_bottom="0",
                padding="0 4em 4em 4em",  # Add padding inside the background
                width="100%",  # Make hstack take full width
                align_self="start",

            ),

            background_color="#FFFBEA",
            width="100%",
            spacing="2",
            height="100%",
            overflow_y="auto",  # Allow scrolling within the content
            overflow_x="auto", # Prevent horizontal overflow
        ),

    )