import reflex as rx
from typing import List, Optional, Dict, Any
from app.components import (SidebarToggle, sidebar, sidebar_expand)
from app.states import MindMapState

class StarToggle(rx.State):
    star: bool = False
    
    def toggle_star(self):
        self.star = not self.star

class TestPracticeOverlay(rx.State):
    show: bool = False
    mode: str = ""  # "test" or "practice"
    
    def open_overlay(self, mode: str):
        """Open the overlay with the specified mode."""
        self.show = True
        self.mode = mode
    
    def close_overlay(self):
        """Close the overlay."""
        self.show = False
    
    def select_option(self, option: str):
        """Handle the selection of a quiz option."""
        # Here you would implement the logic to start the quiz
        # with the selected option (fill-in or multiple-choice)
        print(f"Starting {self.mode} with {option} questions")
        # Close the overlay after selection
        self.close_overlay()

def test_practice_overlay():
    """Create a custom overlay for selecting test/practice type."""
    return rx.cond(
        TestPracticeOverlay.show,
        # When overlay is shown
        rx.box(
            # Transparent overlay background
            rx.box(
                position="fixed",
                top="0",
                left="0",
                width="100%",
                height="100%",
                background_color="rgba(0, 0, 0, 0.5)",
                z_index="998",
                on_click=TestPracticeOverlay.close_overlay,
            ),
            # Popup content
            rx.box(
                rx.vstack(
                    # Header
                    rx.text(
                        f"Choose {TestPracticeOverlay.mode.capitalize()} Type",
                        font_weight="bold",
                        font_size="1.2em",
                        margin_bottom="1em",
                    ),
                    # Option buttons
                    rx.button(
                        "Fill in",
                        on_click=lambda: rx.redirect(f"/fillin?mode_type={TestPracticeOverlay.mode}"),
                        width="100%",
                        background_color="#4CAF50",
                        color="white",
                        margin_bottom="0.5em",
                        padding="0.5em",
                    ),
                    rx.button(
                        "Multiple Choice",
                        on_click=lambda: rx.redirect(f"/choice?mode_type={TestPracticeOverlay.mode}"),
                        width="100%",
                        background_color="#2196F3",
                        color="white",
                        margin_bottom="1em",
                        padding="0.5em",
                    ),
                    # Cancel button
                    rx.button(
                        "Cancel",
                        on_click=TestPracticeOverlay.close_overlay,
                        variant="outline",
                    ),
                    width="100%",
                    align_items="center",
                    padding="1.5em",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width="300px",
                background_color="white",
                border_radius="8px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                z_index="999",
            ),
        ),
        # When overlay is hidden, show nothing
        rx.box()
    )

def heading_section():
    return rx.vstack(
            rx.hstack(
                rx.text(
                    "Feline Evolutionary Tree",
                    size="6",
                    font_weight="bold"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.image(
                                src="/organizeButton.png",
                                width="20px"
                            ),
                            rx.text(
                                "organize",
                                color="black"
                            )
                        ),
                        bg="white"
                    ),
                    rx.button(
                        rx.image(
                            src="/shareButton.png",
                            width="20px"
                        ),
                        bg="white"
                    ),
                    rx.button(
                        rx.image(
                            src="/settingButton.png",
                            width="20px"
                        ),
                        bg="white"
                    ),
                    style={"margin_left": "auto"}
                ),
                margin_y="10px"
            ),
            rx.hstack(
                rx.image(
                    src=rx.cond(StarToggle.star, "/starToggleIcon.png", "/starIcon.png"),
                    width="20px",
                    on_click=StarToggle.toggle_star
                ),
                rx.text(
                    "Add to favourite sets"
                ),
                margin_y="10px"
            ),
            rx.hstack(
                rx.button(
                    "Practice",
                    bg="#FEE381",
                    color="black",
                    width="100px",
                    height="50px",
                    on_click=TestPracticeOverlay.open_overlay("practice"),
                ),
                rx.button(
                    "Test",
                    bg="#FEE381",
                    color="black",
                    width="100px",
                    height="50px",
                    on_click=TestPracticeOverlay.open_overlay("test"),
                ),
                align="center",
                justify="center",
                margin_x="20px"
            ),
            rx.hstack(
                rx.box(
                    width="100px",
                    height="100px",
                    border_radius="100px",
                    bg="#D9D9D9",
                ),
                rx.vstack(
                    rx.text(
                        "create by"
                    ),
                    rx.text(
                        "Prangnaja"
                    )
                )
            )
        )

def render_node(node_id: int):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    MindMapState.get_mindmap[node_id]["text"],
                    width="100%",
                    cursor="pointer",
                    _hover={"background": "#f0f0f0", "border_radius": "4px", "padding": "2px 4px"},
                ),
            ),
        ),
        margin_left=f"{MindMapState.get_mindmap[node_id]["depth"]}em",
        align_items="flex-start",
        width="100%",
    )

def mindmap_view():
    """Render the entire mindmap structure."""
    return rx.box(
        rx.vstack(
            # Render all nodes in display order
            rx.foreach(
                MindMapState.get_display_order,
                lambda node_id: render_node(node_id)
            ),
            spacing="2",
            align_items="flex-start",
            width="80%",
        ),
        padding="1em",
        border_radius="8px",
        width="100%",
        overflow="auto",
    )


def mindmap_page():
    return rx.hstack(
        rx.cond(SidebarToggle.expanded, sidebar_expand(), sidebar()),
        rx.vstack(
            heading_section(),
            mindmap_view(),
            width="100%",
            position="relative",  # Make sure overlay positioning works correctly
        ),
        # Include the overlay component at the end of the layout
        test_practice_overlay(),
        bg="#FFFBEA"
    )