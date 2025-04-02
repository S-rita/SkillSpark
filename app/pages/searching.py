import reflex as rx
from app.components import SidebarToggle, sidebar, sidebar_expand
from app.states import Main_Pages_state




def Top_area():
    return rx.vstack(
        rx.hstack(
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
                outline="none",
                value=Main_Pages_state.search_text,
                on_change=Main_Pages_state.set_search,
                placeholder="Search public mindmaps and contests",
                width="65vw",
                height="100px",
                bg='white',
                style={"& input::placeholder": {"color": "grey", "opacity": "0.25"}},
                border_radius="0.5em",
                color="grey",
                font_size="2em",
                box_shadow="0px 4px 12px rgba(0, 0, 0, 0.25)",
            ),
            rx.button(
                "Search",
                on_click=Main_Pages_state.handle_search_page,  # Add click handler
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
                    "transition": "transform 0.2s ease-in-out"
                }
            ),
            align="center",
            justify_content="space-between",
            width="100%",
            margin_bottom="2em",
        ),
        rx.text(
                f"Results for {(Main_Pages_state.display_text).to_string()}",
                font_size="2em",
                font_weight="bold",
                color="#222222",
                padding="0.5em",
        ),
        rx.box(  # Add horizontal line
            width="100%",  # Match the width of the image box above
            height="1px",  # Line thickness
            bg="#CFCFCF",  # Line color matching text color
            margin_top="0",
            align_self="start",
        ),
        width="100%",

    )
        


def mindmap_item(mindmap: dict[str, str]) -> rx.Component:
    return rx.box(
                rx.vstack(
                    rx.text(mindmap["name"], font_size="1em", font_weight="bold", color="black"),
                    rx.box(
                        f"{mindmap['terms'].to_string()} terms",
                        font_size="0.75em",
                        color="black",
                        background_color="#FFF5D0", 
                        border_radius="1.5em",
                        padding="1px 20px 1px 20px",
                        width="fit-content",
                        height="fit-content",
                        margin_bottom="7em",
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
                    width="100%",
                    height="100%",
                    align_items="start",
                    justify_content="space-between",
                    position="relative",
                    z_index="2"
                ),
                position="relative",
                _before={
                    "content": "''",
                    "position": "absolute",
                    "top": "3em",
                    "right": "0",
                    "width": "70%",
                    "height": "70%",
                    "background_image": "url('/mindmaptail.png')",
                    "background_size": "contain",
                    "background_position": "right center",
                    "background_repeat": "no-repeat",
                    "opacity": "0.1",  # Adjust this value to control opacity (0.0 to 1.0)
                    "z_index": "1"
                },
                background_color="#FFDA5D",
                border_radius="1rem",
                width="100%",
                overflow="hidden", 
                box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                padding="2em 1.5em 2em 1.5em",
                height="100%",
                # bg="green"
            )

def contest_item(mindmap: dict[str, str]) -> rx.Component:
    return rx.box(
                rx.vstack(
                    rx.text(mindmap["name"], font_size="1em", font_weight="bold", color="black"),
                    rx.box(
                        f"{mindmap['sets'].to_string()} sets",
                        font_size="0.75em",
                        color="black",
                        background_color="#FFF5D0",
                        border_radius="1.5em",
                        padding="1px 20px 1px 20px",
                        width="fit-content",
                        height="fit-content",
                        margin_bottom="7em",
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
                    width="100%",
                    height="100%",
                    align_items="start",
                    justify_content="space-between",
                    position="relative",
                    z_index="2"
                ),
                position="relative",
                _before={
                    "content": "''",
                    "position": "absolute",
                    "top": "3em",
                    "right": "2em",
                    "width": "60%",  # Match the background_size you had
                    "height": "60%",
                    "background_image": "url('/champHighBG.png')",
                    "background_size": "contain",
                    "background_position": "right center",
                    "background_repeat": "no-repeat",
                    "opacity": "0.1",  # Adjust this value to control opacity (0.0 to 1.0)
                    "z_index": "1"
                },
                background_color="#FFDA5D",
                border_radius="1rem",
                width="100%",
                overflow="hidden",
                box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                padding="2em 1.5em 2em 1.5em",
                height="100%",
            )

def result_mindmap():
    return rx.vstack(
        rx.hstack(
            rx.text(
                "Mind maps", 
                font_size="1.5em", 
                font_weight="bold",
                color="black",
                align="left",
            ),
            rx.cond(
                Main_Pages_state.has_more_mindmaps,
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
                    on_click=Main_Pages_state.toggle_mindmaps_view,  # For mindmaps
                    _hover={
                        "text_decoration": "none",
                    },
                    style={
                        "transition": "color 0.3s ease-in-out"  # Add transition to base style
                    }
                ),
            ),
            width="100%",
            justify_content="space-between",
            # bg="white",
        ),
        rx.hstack(  # Use grid instead of vstack for the items
            rx.foreach(
                Main_Pages_state.filtered_mindmaps[:3],
                mindmap_item
            ),
            spacing="6",  # Add spacing between grid items
            width="100%",
            height="100%",
            # bg="white",
            align="start",
        ),
        spacing="4",
        padding="0 4em 4em 4em",  # Add padding inside the background
        width="100%",  # Make hstack take full width
        height="100%",
        align_self="left",
        # bg="brown",
    )



def result_contest():
    return rx.vstack(
        rx.hstack(
            rx.text(
                "Contests", 
                font_size="1.5em", 
                font_weight="bold", 
                color="black",
                align="left",
            ),
            rx.cond(
                Main_Pages_state.has_more_contests,
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
                    on_click=Main_Pages_state.toggle_contests_view,  # For contests
                    _hover={
                        "text_decoration": "none",
                    },
                    style={
                        "transition": "color 0.3s ease-in-out"
                    }
                ),
            ),
            width="100%",
            justify_content="space-between",
        ),
        rx.hstack(
            rx.foreach(
                Main_Pages_state.filtered_contests[:3],
                contest_item
            ),
            spacing="6",
            width="100%",
            height="100%",
            align="start",
        ),
        spacing="4",
        padding="0 4em 4em 4em",
        width="100%",
        height="100%",
        align_self="left",
    )

def no_results_message():
    return rx.vstack(
        rx.text(
            "We couldn't find any results.",
            font_size="2.5em",
            font_weight="bold",
            color="black",
            width="100%",
            text_align="center",
        ),
        rx.text(
            "Here are some suggestions to improve your search results:",
            font_size="2em",
            color="gray",
            width="100%",
            text_align="center",
        ),
        rx.vstack(
            rx.text("• Check the spelling or try alternate spellings", color="gray", font_size="1.5em"),
            rx.text("• Search with different keywords", color="gray", font_size="1.5em"),
            rx.text("• Clear your filters", color="gray", font_size="1.5em"),
            spacing="3",
            margin_top="1em",
            align_items="start",
            justify_content="center",
        ),
        width="100%",
        align_items="center",
    )

def result_area():
    return rx.vstack(
        rx.cond(
            Main_Pages_state.check_results == "none",
            no_results_message(),
            rx.cond(
                Main_Pages_state.check_results == "mindmaps_only",
                result_mindmap(),
                rx.cond(
                    Main_Pages_state.check_results == "contests_only", 
                    result_contest(),
                    # If none of above conditions match, show both
                    rx.vstack(
                        result_mindmap(),
                        result_contest(),
                        spacing="4",
                        width="100%",
                        

                    )
                )
            )
        ),
        width="100%",
        # bg="grey",
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



#####!!!!!!!!!!!!!!!  when click view more mindmap

def each_item_Mindmap_search(mindmap: dict[str, str]) -> rx.Component:
    return rx.box(
                rx.vstack(
                    rx.text(mindmap["name"], font_size="1em", font_weight="bold", color="black"),
                    rx.box(
                        f"{mindmap['terms'].to_string()} terms",
                        font_size="0.75em",
                        color="black",
                        background_color="#FFF5D0",
                        border_radius="1.5em",
                        padding="1px 20px 1px 20px",
                        width="fit-content",
                        height="fit-content",
                        margin_bottom="7em",
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
                    width="100%",
                    height="100%",
                    align_items="start",
                    justify_content="space-between",
                    position="relative",
                    z_index="2"
                ),
                position="relative",
                _before={
                    "content": "''",
                    "position": "absolute",
                    "top": "3em",
                    "right": "0",
                    "width": "70%",  # Match the background_size you had
                    "height": "70%",
                    "background_image": "url('/mindmaptail.png')",
                    "background_size": "contain",
                    "background_position": "right center",
                    "background_repeat": "no-repeat",
                    "opacity": "0.1",  # Adjust this value to control opacity (0.0 to 1.0)
                    "z_index": "1"
                },
                background_color="#FFDA5D",
                border_radius="1rem",
                width="100%",
                overflow="hidden",
                box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                padding="2em 1.5em 2em 1.5em",
            )





def mindmaps_full_view() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(
                "Mind maps", 
                font_size="1.5em", 
                font_weight="bold", 
                color="black",
                align="left",
            ),
            rx.link(
                rx.text(
                    "← Back",
                    color="#CAC7BA",
                    font_size="1.5em", 
                    font_weight="bold",
                    _hover={
                        "text_decoration": "none",
                        "color": "#919191",
                        "transition": "color 0.2s ease-in-out"
                    },
                ),
                on_click=Main_Pages_state.toggle_mindmaps_view,
                _hover={
                    "text_decoration": "none",
                },
                style={
                    "transition": "color 0.3s ease-in-out"
                }
            ),
            width="100%",
            justify_content="space-between",
        ),
        rx.grid(
            rx.foreach(
                Main_Pages_state.filtered_mindmaps,
                each_item_Mindmap_search
            ),
            columns="3",
            spacing="6",
            width="100%",
            height="100%",
            align="start",
        ),
        spacing="4",
        padding="0 4em 4em 4em",
        width="100%",
        align_self="left",
    )

#####!!!!!!!!!!!!!!!  when click view more mindmap



#####!!!!!!!!!!!!!!!  when click view more contests

def each_item_contest_search(mindmap: dict[str, str]) -> rx.Component:
    return rx.box(
                rx.vstack(
                    rx.text(mindmap["name"], font_size="1em", font_weight="bold", color="black"),
                    rx.box(
                        f"{mindmap['sets'].to_string()} sets",
                        font_size="0.75em",
                        color="black",
                        background_color="#FFF5D0",
                        border_radius="1.5em",
                        padding="1px 20px 1px 20px",
                        width="fit-content",
                        height="fit-content",
                        margin_bottom="7em",
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
                    width="100%",
                    height="100%",
                    align_items="start",
                    justify_content="space-between",
                    position="relative",
                    z_index="2"
                ),
                position="relative",
                _before={
                    "content": "''",
                    "position": "absolute",
                    "top": "3em",
                    "right": "2em",
                    "width": "60%",  # Match the background_size you had
                    "height": "60%",
                    "background_image": "url('/champHighBG.png')",
                    "background_size": "contain",
                    "background_position": "right center",
                    "background_repeat": "no-repeat",
                    "opacity": "0.1",  # Adjust this value to control opacity (0.0 to 1.0)
                    "z_index": "1"
                },
                background_color="#FFDA5D",
                border_radius="1rem",
                width="100%",
                overflow="hidden",
                box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                },
                padding="2em 1.5em 2em 1.5em",
            )



def contests_full_view() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(
                "Contests", 
                font_size="1.5em", 
                font_weight="bold", 
                color="black",
                align="left",
            ),
            rx.link(
                rx.text(
                    "← Back",
                    color="#CAC7BA",
                    font_size="1.5em",
                    font_weight="bold",
                    _hover={
                        "text_decoration": "none",
                        "color": "#919191",
                        "transition": "color 0.2s ease-in-out"
                    },
                ),
                on_click=Main_Pages_state.toggle_contests_view,
                _hover={
                    "text_decoration": "none",
                },
                style={
                    "transition": "color 0.3s ease-in-out"
                }
            ),
            width="100%",
            justify_content="space-between",
        ),
        rx.grid(
            rx.foreach(
                Main_Pages_state.filtered_contests,
                each_item_contest_search
            ),
            columns="3",
            spacing="6",
            width="100%",
            height="100%",
            align="start",
        ),
        spacing="4",
        padding="0 4em 4em 4em",
        width="100%",
        align_self="left",
    )
#####!!!!!!!!!!!!!!!  when click view more contests





def searching_page() -> rx.Component:
    return layout( 
        rx.vstack(
            Top_area(),
            rx.cond(
                Main_Pages_state.show_mindmaps_full,
                mindmaps_full_view(),
                rx.cond(
                    Main_Pages_state.show_contests_full,
                    contests_full_view(),
                    result_area(),
                ),
            ),
            spacing="9",
            background_color="#FFFBEA",
            padding="4em 4em 4em 4em",
            width="100%",
            height="100%",
            overflow_y="auto",  # Allow scrolling within the content
            overflow_x="auto", # Prevent horizontal overflow
        )
    )