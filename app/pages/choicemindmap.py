import reflex as rx
import random
from typing import List, Optional, Dict, Any

class ChoiceMindmapState(rx.State):
    # Default mode if not specified
    mode: str = "practice"

    def on_load(self):
        """This runs when the page loads and can access route params"""
        # Get mode from route parameters if available
        route_mode = self.router.page.params.get("mode")
        if route_mode:
            self.mode = route_mode

class MindMapMultipleChoice(rx.State):
    mindmap: Dict[int, Dict[str, Any]] = {
        0: {"text": "Feline", "parent": None, "depth": 0},
        1: {"text": "Tiger", "parent": 0, "depth": 1},
        2: {"text": "Lion", "parent": 0, "depth": 1},
        3: {"text": "Domestic", "parent": 0, "depth": 1},
        4: {"text": "Wild", "parent": 0, "depth": 1},
        5: {"text": "Cat", "parent": 3, "depth": 2},
    }
    
    question_nodes: List[int] = []  # Changed to list for easier popping
    current_question: Optional[int] = None
    current_question_text: str = ""  # Added to store the text of current question
    answer_options: List[str] = []
    selected_answer: Optional[str] = None
    score: int = 0
    total_questions: int = 0
    questions_answered: int = 0
    game_active: bool = False  # Track if game is active
    game_complete: bool = False  # Track if game is finished
    
    def start_game(self):
        """Initialize the multiple-choice game."""
        non_root_nodes = [node_id for node_id, data in self.mindmap.items() if data.get("parent") is not None]
        num_questions = max(1, len(non_root_nodes) * 7 // 10)  # 70% of non-root nodes
        self.question_nodes = random.sample(non_root_nodes, num_questions)
        self.total_questions = len(self.question_nodes)
        self.questions_answered = 0
        self.score = 0
        self.game_active = True
        self.game_complete = False
        self.next_question()
    
    def next_question(self):
        """Move to the next question if available."""
        if not self.question_nodes:
            # No more questions - end the game
            self.current_question = None
            self.current_question_text = ""
            self.answer_options = []
            self.game_active = False
            self.game_complete = True
            return
        
        self.current_question = self.question_nodes.pop()  # Works with a list
        self.current_question_text = self.mindmap[self.current_question]["text"]
        
        correct_parent_id = self.mindmap[self.current_question]["parent"]
        correct_parent_text = self.mindmap[correct_parent_id]["text"]
        
        # Get all unique parent texts except None
        all_parent_texts = set()
        for node_id, data in self.mindmap.items():
            parent_id = data.get("parent")
            if parent_id is not None:
                parent_text = self.mindmap[parent_id]["text"]
                all_parent_texts.add(parent_text)
        
        # Remove the correct parent from possible incorrect answers
        all_possible_parents = list(all_parent_texts)
        if correct_parent_text in all_possible_parents:
            all_possible_parents.remove(correct_parent_text)
        
        # Select random incorrect answers
        num_options = min(3, len(all_possible_parents))
        incorrect_answers = random.sample(all_possible_parents, num_options) if all_possible_parents else []
        
        self.answer_options = incorrect_answers + [correct_parent_text]
        random.shuffle(self.answer_options)
        
        self.selected_answer = None
    
    def select_answer(self, answer: str):
        """Handle user selecting an answer."""
        self.selected_answer = answer
        correct_parent_id = self.mindmap[self.current_question]["parent"]
        correct_parent_text = self.mindmap[correct_parent_id]["text"]
        
        if answer == correct_parent_text:
            self.score += 1
        
        self.questions_answered += 1
        self.next_question()
    
    def exit_game(self):
        """Exit game mode and reset state."""
        self.question_nodes = []
        self.current_question = None
        self.current_question_text = ""
        self.answer_options = []
        self.selected_answer = None
        self.game_active = False
        self.game_complete = False

def question_display():
    """Render the current multiple-choice question."""
    return rx.box(
        rx.vstack(
            # Game active with questions
            rx.cond(
                MindMapMultipleChoice.game_active,
                rx.vstack(
                    rx.text(
                        f"What is the parent of '{MindMapMultipleChoice.current_question_text}'?",
                        font_weight="bold",
                    ),
                    rx.foreach(
                        MindMapMultipleChoice.answer_options,
                        lambda option: rx.button(
                            option,
                            on_click=MindMapMultipleChoice.select_answer(option),
                            variant="outline",
                            margin="5px",
                        ),
                    ),
                    rx.hstack(
                        rx.text("Score: "),
                        rx.text(MindMapMultipleChoice.score),
                        rx.text("/"),
                        rx.text(MindMapMultipleChoice.total_questions),
                    ),
                    rx.hstack(
                        rx.text("Questions: "),
                        rx.text(MindMapMultipleChoice.questions_answered),
                        rx.text("/"),
                        rx.text(MindMapMultipleChoice.total_questions),
                    ),
                ),
                # Game complete or not started
                rx.vstack(
                    rx.cond(
                        MindMapMultipleChoice.game_complete,
                        rx.text("Game Complete!", font_weight="bold", font_size="xl"),
                        rx.text("Start the game to play", font_weight="bold"),
                    ),
                    rx.cond(
                        MindMapMultipleChoice.game_complete,
                        rx.vstack(
                            rx.hstack(
                                rx.text("Final Score: ", font_weight="medium"),
                                rx.text(MindMapMultipleChoice.score),
                                rx.text("/"),
                                rx.text(MindMapMultipleChoice.total_questions),
                            ),
                            rx.button(
                                "Play Again", 
                                on_click=MindMapMultipleChoice.start_game,
                                color_scheme="green",
                                margin_top="10px",
                            ),
                        ),
                        rx.text(""),
                    ),
                ),
            ),
        ),
        padding="20px",
        background="#f0f0f0",
        border_radius="10px",
        width="100%",
    )

def choicemindmap_page():
    """Render the entire multiple-choice mindmap game page."""
    return rx.container(
        rx.vstack(
            rx.heading(f"Multiple Choice - {ChoiceMindmapState.mode.capitalize()} Mode"),
            rx.cond(
                ~MindMapMultipleChoice.game_active & ~MindMapMultipleChoice.game_complete,
                rx.button(
                    "Start Game", 
                    on_click=MindMapMultipleChoice.start_game, 
                    margin_bottom="10px",
                    color_scheme="blue",
                    size="3",
                ),
                rx.text(""),
            ),
            question_display(),
        ),
        padding="20px",
        max_width="800px",
        on_mount=ChoiceMindmapState.on_load
    )