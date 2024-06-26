from enum import Enum

from utils.Exceptions import NoMatchingStateException


class State(Enum):
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
    try:
        return State(state_string)
    except ValueError:
        raise NoMatchingStateException(f'no matching state for string: {state_string}')