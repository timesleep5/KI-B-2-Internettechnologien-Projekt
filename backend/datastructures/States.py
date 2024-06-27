from enum import Enum
from utils.Exceptions import NoMatchingStateException


class State(Enum):
    """
    Enumeration defining possible states of a chatbot.

    Enum Values:
        START: Starting state.
        RESTART: State to restart the chat.
        HELP: State to request help.
        LOAD_SUMMARY: State to load a summary.
        SUMMARY_OVERVIEW: State to overview a summary.
        SHOW_LOADED_SUMMARY: State to show a loaded summary.
        INPUT_STARTDATE: State to input a start date.
        INPUT_MONTHS: State to input months.
        INPUT_KM_LIMIT: State to input a kilometer limit.
        INPUT_KM_DRIVEN: State to input kilometers driven.
        ASK_FOR_CHANGES: State to ask for changes.
        CHANGES: State to apply changes.
        SHOW_SUMMARY: State to show a summary.
        SAVE_SUMMARY: State to save a summary.
        EXIT: State to exit the chat or process.

    """
    START = 'start'
    RESTART = 'restart'
    HELP = 'help'
    LOAD_SUMMARY = 'load_summary'
    SUMMARY_OVERVIEW = 'summary_overview'
    SHOW_LOADED_SUMMARY = 'show_loaded_summary'
    INPUT_STARTDATE = 'input_startdate'
    INPUT_MONTHS = 'input_months'
    INPUT_KM_LIMIT = 'input_km_limit'
    INPUT_KM_DRIVEN = 'input_km_driven'
    ASK_FOR_CHANGES = 'ask_for_changes'
    CHANGES = 'changes'
    SHOW_SUMMARY = 'show_summary'
    SAVE_SUMMARY = 'save_summary'
    EXIT = 'exit'


def get_state(state_string: str) -> State:
    """
    Converts a string representation to a State enum value.

    Args:
        state_string (str): String representation of a State.

    Returns:
        State: Corresponding State enum value.

    Raises:
        NoMatchingStateException: If no matching State enum value is found for the provided string.
    """
    try:
        return State(state_string)
    except ValueError:
        raise NoMatchingStateException(f'no matching state for string: {state_string}')
