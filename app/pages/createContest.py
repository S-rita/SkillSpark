import reflex as rx
from app.states import CreateContestState
from app.components import sidebar_view

def mindmap_item(m):
    return rx.hstack(
        rx.checkbox(
            is_checked=CreateContestState.is_selected(m),
            on_change=lambda checked: CreateContestState.toggle_mindmap_selection_by_id(m["mindmap_id"]),
        ),
        rx.text(f"{m['name']} ({m['terms']} terms)", color="black"),
    )

def createcontest_page():
    date_input_style = {
        "background_color": "white",
        "height": "50px",
        "width": "100px",
        "color": "black", 
        "padding": "10px",
        "border_radius": "8px",
        "border_width": "1px",
        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px"
    }

    return rx.hstack(
        sidebar_view(),
        rx.box(
            rx.vstack(
                rx.box(
                    rx.link(
                        rx.text("X", font_size="40px", color="#333", text_align="center", weight="medium"),
                        href="/contest",
                    ),
                    position="absolute",
                    top="35px",
                    right="50px",
                    background_color="#FDCC00",
                    border_radius="12px",
                    width="55px",
                    height="55px",
                    border="1px solid black",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    box_shadow=" 0px 2px 4px rgba(0, 0, 0, 0.2)",
                    _hover={"background_color": "#CBA300", "cursor": "pointer"}
                ),

                rx.heading(
                    "Create a New Contest",
                    padding_bottom="1em",
                    color="black",
                    font_size="56px",
                    margin_top="20px",
                ),

                rx.input(
                    placeholder="Contest Name",
                    value=CreateContestState.contest_name,
                    on_change=CreateContestState.set_contest_name,
                    style={
                        "background_color": "#F5F5F5",
                        "height": "70px",
                        "width": "1000px",
                        "font_size": "24px",
                        "color": "#464545",
                        "padding": "10px",
                        "border_radius": "8px",
                        "border_width": "1px", 
                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        "& input::placeholder": {
                            "color": "#808080",
                            "opacity": 1
                        }
                    },
                    margin_top="-20px",
                ),

                rx.text_area(
                    placeholder="Description",
                    value=CreateContestState.description,
                    on_change=CreateContestState.set_description,
                    style={
                        "background_color": "#F5F5F5",
                        "height": "70px",
                        "width": "1000px",
                        "font_size": "24px",
                        "color": "#464545",
                        "padding": "10px",
                        "border_radius": "8px",
                        "border_width": "1px",
                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        "& textarea::placeholder": {
                            "color": "#808080",
                            "opacity": 1
                        }
                    },
                    min_height="100px"
                ),

                rx.hstack(
                    # Start Date section
                    rx.vstack(
                        rx.text("Start Date", font_weight="500", style={"color": "#3E3E3E", "font_size": "18px", "margin_bottom": "-10px"}),
                        rx.hstack(
                            rx.select(
                                items=[str(i) for i in range(1, 32)],
                                value=CreateContestState.start_day,
                                on_change=CreateContestState.set_start_day,
                                placeholder="Day",
                                style=date_input_style
                            ),
                            rx.select(
                                CreateContestState.month_names,
                                placeholder="Month",
                                value=CreateContestState.display_month,  # Use the computed display value
                                on_change=CreateContestState.set_start_month,
                                style=date_input_style
                            ),
                            
                            rx.select(
                                items=[str(year) for year in range(2025, 2036)],
                                value=CreateContestState.start_year,
                                on_change=CreateContestState.set_start_year,
                                placeholder="Year",
                                style=date_input_style
                            ),
                            spacing="4"
                        ),
                        margin_right="50px",
                    ),
                    
                    # Due Date section
                    rx.vstack(
                        rx.text("Due Date", font_weight="500", style={"color": "#3E3E3E", "font_size": "18px", "margin_bottom": "-10px"}),
                        rx.hstack(
                            rx.select(
                                items=[str(i) for i in range(1, 32)],
                                value=CreateContestState.due_day,
                                on_change=CreateContestState.set_due_day,
                                placeholder="Day",
                                style=date_input_style
                            ),
                            rx.select(
                                CreateContestState.month_names,
                                placeholder="Month", 
                                value=CreateContestState.display_due_month,
                                on_change=CreateContestState.set_due_month,
                                style=date_input_style
                            ),
                            rx.select(
                                items=[str(year) for year in range(2025, 2036)],
                                value=CreateContestState.due_year,
                                on_change=CreateContestState.set_due_year,
                                placeholder="Year",
                                style=date_input_style
                            ),
                            spacing="4"
                        )
                    ),
                ),

                rx.text("Select mind maps", font_weight="500", style={"color": "#3E3E3E", "font_size": "18px", "margin_bottom": "-10px"}),
                rx.box(
                    rx.foreach(
                        CreateContestState.available_mindmaps,
                        lambda m: rx.box(
                            mindmap_item(m),
                            margin_top="1em",  # adds spacing between items
                            margin_bottom="1em"  # adds spacing between items
                        )
                    ),
                    padding="1em",
                    background="white",
                    border_radius="8px",
                    box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
                    width="100%"
                ),

                rx.cond(
                    CreateContestState.error_message != "",
                    rx.text(CreateContestState.error_message, color="red")
                ),
                rx.cond(
                    CreateContestState.success_message != "",
                    rx.text(CreateContestState.success_message, color="green")
                ),

                rx.button(
                    "Create Contest",
                    on_click=lambda: CreateContestState.create_contest("user123"),
                    background_color="#FDCC00",
                    color="black",
                    height="50px",
                    width="300px",
                    font_size="20px",
                    weight="bold",
                    padding="10px 20px", 
                    border_radius="8px",
                    _hover={"background_color": "#FFDA5D"},
                    box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
                ),

                spacing="4",
                align="start",
                width="100%",
                max_width="800px"
            ),
            background_color="#fffbe6",
            padding="40px",
            height="100vh", 
            overflow_y="auto",
            flex="1",
            on_mount=CreateContestState.reset_input,
        ),
        align="start",
        spacing="0",
    )
