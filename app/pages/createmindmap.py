import reflex as rx
from typing import List, Optional, Dict, Any
from app.states import MindMapState
from app.components import (sidebar, sidebar_expand, SidebarToggle)

class AccessButtonToggle(rx.State):
    private: bool = True
    
    def toggle_button(self):
        self.private = not self.private

def render_node(node_id: int):
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Show input field if this node is being edited
                rx.cond(
                    MindMapState.editing_node_id == node_id,
                    rx.hstack(
                        rx.input(
                            value=MindMapState.editing_text,
                            on_change=MindMapState.handle_edit_change,
                            width="100%",
                            auto_focus=True,
                        ),
                        rx.button(
                            "Save",
                            on_click=MindMapState.save_editing,
                            size="2",
                            bg="#FFDA5D",
                            color="black"
                        ),
                        rx.button(
                            "Cancel",
                            on_click=MindMapState.cancel_editing,
                            size="2",
                            variant="outline",
                            bg="#FFDA5D",
                            color="black"
                        ),
                        width="100%",
                    ),
                    # Show regular text with double-click to edit
                    rx.text(
                        MindMapState.get_mindmap[node_id]["text"],
                        width="100%",
                        cursor="pointer",
                        # Use double-click to edit
                        on_double_click=MindMapState.start_editing(node_id),
                        # Add visual cue
                        _hover={"background": "#f0f0f0", "border_radius": "4px", "padding": "2px 4px"},
                    ),
                ),
                rx.spacer(),
                rx.button(
                    "Delete", 
                    on_click=MindMapState.delete_node(node_id),
                    size="2",
                    bg="#FFDA5D",
                    color="black"
                ),
                rx.button(
                    "Add Child", 
                    on_click=MindMapState.add_child(node_id),
                    size="2",
                    bg="#FFDA5D",
                    color="black"
                ),
            ),
            margin_left=f"{MindMapState.get_mindmap[node_id]['depth']}em",
            align_items="flex-start",
            width="100%",
        )
    )

def mindmap_view():
    """Render the entire State structure."""
    return rx.box(
        rx.vstack(
            # Render all nodes in display order
            rx.foreach(
                MindMapState.get_display_order,
                lambda node_id: render_node(node_id)
            ),
            spacing="2",
            align_items="flex-start",
            width="100%",
        ),
        padding="1em",
        border_radius="8px",
        width="100%",
        overflow="auto",
    )

def createheading_section():
    return rx.vstack(
            rx.hstack(
                rx.heading("Create a new MindMap set"),
                rx.spacer(), 
                rx.button(
                    "Create",
                    on_click=MindMapState.handle_createMindMap,
                    bg="#FFDA5D",
                    color="black",
                    border_color="#9A9A9A",
                    border_radius="10px",
                    style={"margin_left": "auto"}
                ),
                width="100%",
                align_items="center",
                justify_content="space-between"
            ),
            rx.input(
                placeholder="Enter Title",
                value=MindMapState.mindmap_name,
                on_change=MindMapState.set_mindmap_name,
                width="80%"
            ),
            rx.text_area(
                placeholder="Add a description...",
                value=MindMapState.mindmap_description,
                on_change=MindMapState.set_mindmap_description,
                width="80%"
            ),
            rx.hstack(
                rx.text("Theme: "),
                rx.spacer(),
                rx.button(
                    rx.cond(AccessButtonToggle.private, "private", "public"),
                    on_click=AccessButtonToggle.toggle_button,
                    bg="white",
                    color="black",
                    style={"margin_left": "auto"}
                ),
                width="100%",
                align_items="center",
                justify_content="space-between"
            ),
            width="100%"
        )

def createmindmap_section():
    return rx.box(
        rx.vstack(
            rx.box(
                rx.text(
                    "Double-click on any node text to edit",
                    font_style="italic",
                    color="gray",
                    font_size="sm",
                    margin_bottom="8px",
                ),
            ),
            mindmap_view(),
            rx.hstack(
                rx.button(
                    "+", 
                    on_click=MindMapState.add_child(None),
                    margin_top="10px",
                    bg="#FFDA5D",
                    color="black"
                ),
            ),
        ),
        padding="20px",
        border_radius="10px",
        width="100%",
        overflow="auto",
    )

def createmindmap_page():
    return rx.hstack(
        rx.cond(SidebarToggle.expanded, sidebar_expand(), sidebar()),
        rx.vstack(
            createheading_section(),
            createmindmap_section(),
            padding_y="50px",
            padding_x="50px",
            width="100%"
        ),
        width="100%",
        height="100vh",
        bg="#FFFBEA"
    )