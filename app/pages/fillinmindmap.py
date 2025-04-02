import reflex as rx
import random
from typing import List, Optional, Dict, Any, Set

class FillinMindmapState(rx.State):
    # Default mode if not specified
    mode: str = "practice"

    def on_load(self):
        """This runs when the page loads and can access route params"""
        # Get mode from route parameters if available
        route_mode = self.router.page.params.get("mode")
        if route_mode:
            self.mode = route_mode

class MindMapFillIn(rx.State):
    mindmap: Dict[int, Dict[str, Any]] = {
        0: {"text": "Feline", "parent": None, "depth": 0},
        1: {"text": "Tiger", "parent": 0, "depth": 1},
        2: {"text": "Lion", "parent": 0, "depth": 1},
        3: {"text": "Domestic", "parent": 0, "depth": 1},
        4: {"text": "Wild", "parent": 0, "depth": 1},
        5: {"text": "Cat", "parent": 3, "depth": 2},
    }
    # Add a counter to force refresh
    update_counter: int = 0
    
    # Game specific variables
    hidden_nodes: Set[int] = set()
    current_page: int = 1
    total_pages: int = 1
    selected_word: Optional[str] = None
    available_words: List[str] = []
    
    def start_game(self):
        """Initialize game by hiding random nodes"""
        # Get non-root nodes that can be hidden
        non_root_nodes = [node_id for node_id, data in self.mindmap.items() 
                          if data.get("parent") is not None]
        
        # Determine how many nodes to hide (around 40-60% of non-root nodes)
        num_to_hide = max(1, len(non_root_nodes) // 2)
        
        # Randomly select nodes to hide
        self.hidden_nodes = set(random.sample(non_root_nodes, num_to_hide))
        
        # Create available words list (includes correct answers plus some decoys)
        self.available_words = []
        for node_id in self.hidden_nodes:
            self.available_words.append(self.mindmap[node_id]["text"])
        
        # Shuffle the words
        random.shuffle(self.available_words)
        
        # Set current page
        self.current_page = 1
        self.total_pages = len(self.hidden_nodes)
        
        self.trigger_update()
    
    def select_word(self, word: str):
        """Handle word selection"""
        self.selected_word = word
    
    def check_answer(self, node_id: int):
        """Check if selected word is correct for the given node"""
        if self.selected_word is None:
            return False
        
        correct_answer = self.mindmap[node_id]["text"]
        return self.selected_word == correct_answer
    
    def reveal_node(self, node_id: int):
        """Reveal a hidden node if the answer is correct"""
        if node_id in self.hidden_nodes and self.check_answer(node_id):
            self.hidden_nodes.remove(node_id)
            
            # Remove the word from available_words
            if self.selected_word in self.available_words:
                self.available_words.remove(self.selected_word)
                
            self.selected_word = None
            
            # Update page count
            self.current_page = self.total_pages - len(self.hidden_nodes)
            
            # Check if game is complete
            if not self.hidden_nodes:
                # Game completed!
                pass
                
            self.trigger_update()
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
    
    def trigger_update(self):
        """Increment counter to force re-rendering"""
        self.update_counter += 1
    
    @rx.var(cache=True)
    def get_mindmap(self) -> Dict[int, Dict[str, Any]]:
        """Returns a copy of the mindmap to prevent recursion errors."""
        # Use update_counter to invalidate cache when needed
        _ = self.update_counter
        return {k: v.copy() for k, v in self.mindmap.items()}
    
    @rx.var(cache=True)
    def get_children(self) -> Dict[int, List[int]]:
        """Dynamically compute children based on current parent relationships."""
        # Use update_counter to invalidate cache when needed
        _ = self.update_counter
        
        children = {}
        # Initialize all nodes with empty children lists
        for node_id in self.mindmap:
            children[node_id] = []
            
        # Populate children lists based on parent relationships
        for node_id, node_data in self.mindmap.items():
            parent_id = node_data.get("parent")
            if parent_id is not None and parent_id in children:
                children[parent_id].append(node_id)
                
        return children
    
    @rx.var(cache=True)
    def get_root_nodes(self) -> List[int]:
        """Return a list of root node IDs (nodes with no parent)."""
        # Use update_counter to invalidate cache when needed
        _ = self.update_counter
        
        return [node_id for node_id, data in self.mindmap.items() 
                if data.get("parent") is None]
    
    @rx.var(cache=True)
    def get_display_order(self) -> List[int]:
        """Return the correct order to display nodes in a depth-first manner."""
        # Use update_counter to invalidate cache when needed
        _ = self.update_counter
        
        def traverse(node_id: int, order: List[int]):
            """Recursive function to process nodes in depth-first order."""
            order.append(node_id)  # Add the current node first
            for child_id in self.get_children.get(node_id, []):  # Get children safely
                traverse(child_id, order)  # Recursively add child nodes

        display_order = []
        for root_id in self.get_root_nodes:  # Start with root nodes
            traverse(root_id, display_order)

        return display_order
    
    def exit_game(self):
        """Exit game mode and reset game state"""
        self.hidden_nodes = set()
        self.selected_word = None
        self.trigger_update()
        # In a real app, this would navigate back to the creator view

def render_node_game_mode(node_id: int):
    """Render a node in game mode with hidden nodes"""
    # Determine if this node is hidden
    is_hidden = MindMapFillIn.hidden_nodes.contains(node_id)
    
    # Check if selected word is correct for this node (if hidden)
    is_correct = rx.cond(
        (MindMapFillIn.selected_word is not None) & is_hidden,
        MindMapFillIn.check_answer(node_id),
        False
    )
    
    node_style = {
        "border": "2px solid black",
        "border_radius": "15px",
        "padding": "5px 15px",
        "margin": "2px",
        "background": rx.cond(
            is_hidden,
            rx.cond(
                is_correct,
                "#90EE90",  # Light green for correct answer
                "#FFCCCB"   # Light red for incorrect/unanswered
            ),
            "white"
        )
    }
    
    return rx.box(
        rx.hstack(
            # Node content
            rx.cond(
                is_hidden,
                rx.center(
                    rx.text(
                        "?",
                        font_size="1.2em",
                        font_weight="bold",
                    ),
                    width="100%",
                    on_click=MindMapFillIn.reveal_node(node_id),
                    cursor="pointer",
                ),
                rx.text(
                    MindMapFillIn.mindmap[node_id]["text"],
                    font_weight="medium",
                )
            ),
            margin_left=f"{MindMapFillIn.mindmap[node_id]['depth']}em",
            align_items="center",
            width="fit-content",
            **node_style
        )
    )

def word_selection_area():
    """Render the word selection area at the bottom of the game view"""
    return rx.box(
        rx.vstack(
            rx.text(
                "Words Available:",
                font_weight="bold",
                align_self="flex-start",
                margin_bottom="5px",
            ),
            rx.box(
                rx.foreach(
                    MindMapFillIn.available_words,
                    lambda word: rx.button(
                        word,
                        on_click=MindMapFillIn.select_word(word),
                        variant=rx.cond(
                            MindMapFillIn.selected_word == word,
                            "solid",
                            "outline"
                        ),
                        margin="2px",
                        size="2",
                    )
                ),
                spacing="2",
            ),
        ),
        padding="10px",
        background="#f0f0f0",
        border_radius="5px",
        margin_top="20px",
        width="100%",
    )

def game_header():
    """Render the game header with page info and close button"""
    return rx.hstack(
        rx.button(
            "Fill-in",
            variant="solid",
            size="2",
            is_disabled=True,
            background="#F0E68C",
            border_radius="0",
            margin_right="5px",
        ),
        rx.icon("chevron-down", color="black"),
        rx.spacer(),
        rx.text(
            f"{MindMapFillIn.current_page}/{MindMapFillIn.total_pages}",
            font_weight="bold",
        ),
        rx.spacer(),
        rx.button(
            "×",
            on_click=MindMapFillIn.exit_game,
            size="2",
            color="black",
            background="#FFD700",
            border_radius="0",
        ),
        padding="5px",
        background="#F0E68C",
        width="100%",
    )

def mindmap_game_view():
    return rx.box(
        rx.vstack(
            game_header(),
            rx.box(
                rx.vstack(
                    rx.foreach(
                        MindMapFillIn.get_display_order,
                        lambda node_id: render_node_game_mode(node_id)
                    ),
                    align_items="flex-start",
                    width="100%",
                    spacing="3",
                    padding="15px",
                ),
                background="#FFF8DC",  # Cream background
                border_radius="10",
                width="100%",
                height="80%",
                overflow="auto",
            ),
            word_selection_area(),
            width="100%",
        ),
        border="1px solid #FFD700",
        background="#FFFACD",  # Light yellow background
        width="100%",
    )


def fillinmindmap_page():
    return rx.container(
        rx.vstack(
            rx.button(
                "Start Game",
                on_click=MindMapFillIn.start_game,
                size="3",
                variant="solid",
                background="#32CD32",  # Lime green button
                color="white",
                padding="10px 20px",
                border_radius="10px",
            ),
            mindmap_game_view(),
            align_items="center",
            justify_content="center",
            width="100%",
        ),
        width="100%",
        height="100vh",
        overflow="auto",
        background="#FFFACD",  # Light yellow background
    )

