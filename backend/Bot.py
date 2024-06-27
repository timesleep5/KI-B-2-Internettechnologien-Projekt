import random
from datetime import datetime
from typing import List, Dict

from SummaryBuilder import SummaryBuilder
from datastructures.ChatModels import Message, User
from datastructures.States import State, get_state
from datastructures.SummaryData import SummaryData
from utils.Exceptions import NoKeywordFoundException, NoMatchingStateException
from utils.fs_utils import read_json, Paths, saved_summary_ids, \
    save_json, read_summary_with_id
from utils.regex_utils import find_number, find_date, find_summary_id


class Bot:
    """
    Represents a chatbot that interacts with users to manage leasing summaries.

    Attributes:
        __summary_data (SummaryData): Instance to manage summary-related data.
        __state (State): Current state of the chatbot.
        __previous_state (State): Previous state of the chatbot.
        __questions (Dict[str, List[str]]): Dictionary storing questions for different states.
        __fallbacks (List[str]): List of fallback responses.
        __transitions (Dict[str, Dict[str, str]]): Dictionary mapping transitions between states.
        __saved_summaries (List[int]): List of IDs of saved summaries.
        __needs_additional_info (List[State]): States requiring additional user information.
        __loaded_summary_id (int): ID of the currently loaded summary.
        __saved_summary_id (int): ID of the saved summary.
        __summary_builder (SummaryBuilder): Instance to build summary reports.
    """

    def __init__(self):
        """
        Initializes a Bot instance, setting up initial states, loading JSON data,
        and preparing necessary attributes.
        """
        self.__summary_data = SummaryData()

        self.__state: State = State.START
        self.__previous_state: State = State.START

        self.__questions: Dict[str, List[str]]
        self.__fallbacks: List[str]
        self.__transitions: Dict[str, Dict[str, str]]

        self.__saved_summaries: List[int]

        self.__needs_additional_info = [
            State.SUMMARY_OVERVIEW,
            State.SHOW_LOADED_SUMMARY,
            State.ASK_FOR_CHANGES,
            State.SHOW_SUMMARY,
            State.SAVE_SUMMARY
        ]

        self.__loaded_summary_id: int
        self.__saved_summary_id: int
        self.__summary_builder: SummaryBuilder

        self.__load_jsons()
        self.__update_saved_summaries()

    def __load_jsons(self) -> None:
        """
        Loads JSON data files into corresponding attributes (__questions, __fallbacks,
        __transitions, __greetings) from predefined paths.
        """
        self.__questions = read_json(Paths.BOT_QUESTIONS)
        self.__fallbacks = read_json(Paths.BOT_FALLBACKS)
        self.__transitions = read_json(Paths.BOT_TRANSITIONS)
        self.__greetings = read_json(Paths.BOT_GREETINGS)

    def get_greeting(self) -> Message:
        """
        Generates a random greeting message.

        Returns:
            Message: Bot message containing the greeting.
        """
        message = random.choice(self.__greetings)
        return self.__build_response(message)

    def get_start_message(self) -> Message:
        """
        Generates the initial message when starting the conversation.

        Returns:
            Message: Bot message containing the start message.
        """
        message = self.__random_question_of_current_state()
        return self.__build_response(message)

    def respond_to(self, message: Message) -> Message:
        """
        Responds to the user message based on the current state.

        Args:
            message (Message): User message containing the user input.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        content = message.content.lower()
        match self.__state:
            case State.START:
                return self.__handle_start(content)

            case State.RESTART:
                return self.__handle_restart(content)

            case State.HELP:
                return self.__handle_help()

            case State.LOAD_SUMMARY:
                return self.__handle_load_summary(content)

            case State.SUMMARY_OVERVIEW:
                return self.__handle_summary_overview(content)

            case State.SHOW_LOADED_SUMMARY:
                return self.__handle_show_loaded_summary(content)

            case State.INPUT_STARTDATE:
                return self.__handle_input_startdate(content)

            case State.INPUT_MONTHS:
                return self.__handle_input_months(content)

            case State.INPUT_KM_LIMIT:
                return self.__handle_input_km_limit(content)

            case State.INPUT_KM_DRIVEN:
                return self.__handle_input_km_driven(content)

            case State.ASK_FOR_CHANGES:
                return self.__handle_ask_for_changes(content)

            case State.CHANGES:
                return self.__handle_changes(content)

            case State.SHOW_SUMMARY:
                return self.__handle_show_summary(content)

            case State.SAVE_SUMMARY:
                return self.__handle_save_summary()

            case State.EXIT:
                return self.__handle_exit(content)

            case _:
                return self.__handle_unknown_state()

    def __handle_start(self, content: str) -> Message:
        """
        Handles user input during the START state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        self.__update_saved_summaries()
        try:
            new_state_string = self.__spot_keywords_for_new_state(content)
            new_state = get_state(new_state_string)
            if new_state == State.LOAD_SUMMARY and not self.__saved_summaries:
                return self.__switch_state_and_respond(State.INPUT_STARTDATE)
            return self.__switch_state_and_respond(new_state)
        except NoKeywordFoundException:
            return self.__random_fallback_response()
        except NoMatchingStateException:
            # TODO log
            return self.__random_fallback_response()

    def __handle_restart(self, content: str) -> Message:
        """
        Handles user input during the RESTART state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            new_state_string = self.__spot_keywords_for_new_state(content)
            if new_state_string == 'previous':
                return self.__switch_to_previous_and_respond()
            else:
                new_state = get_state(new_state_string)
                return self.__switch_state_and_respond(new_state)
        except NoKeywordFoundException:
            return self.__random_fallback_response()
        except NoMatchingStateException:
            # TODO log
            return self.__random_fallback_response()

    def __handle_help(self) -> Message:
        """
        Handles user input during the HELP state.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        return self.__switch_to_previous_and_respond()

    def __handle_load_summary(self, content: str) -> Message:
        """
        Handles user input during the LOAD_SUMMARY state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_summary_overview(self, content: str) -> Message:
        """
        Handles user input during the SUMMARY_OVERVIEW state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            self.__loaded_summary_id = find_summary_id(content)
            return self.__switch_state_and_respond(State.SHOW_LOADED_SUMMARY)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_show_loaded_summary(self, content: str) -> Message:
        """
        Handles user input during the SHOW_LOADED_SUMMARY state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_input_startdate(self, content: str) -> Message:
        """
        Handles user input during the INPUT_STARTDATE state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            startdate = find_date(content)
            self.__summary_data.set_start_date(startdate)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_MONTHS)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_input_months(self, content: str) -> Message:
        """
        Handles user input during the INPUT_MONTHS state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            months = find_number(content)
            self.__summary_data.set_months(months)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_KM_LIMIT)
        except ValueError:
            self.__response_without_functionality(content)

    def __handle_input_km_limit(self, content: str) -> Message:
        """
        Handles user input during the INPUT_KM_LIMIT state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            km_limit = find_number(content)
            self.__summary_data.set_km_limit(km_limit)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_KM_DRIVEN)
        except ValueError:
            self.__response_without_functionality(content)

    def __handle_input_km_driven(self, content: str) -> Message:
        """
        Handles user input during the INPUT_KM_DRIVEN state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            km_driven = find_number(content)
            self.__summary_data.set_km_driven(km_driven)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.ASK_FOR_CHANGES)
        except ValueError:
            self.__response_without_functionality(content)

    def __handle_ask_for_changes(self, content: str) -> Message:
        """
        Handles user input during the ASK_FOR_CHANGES state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_changes(self, content: str) -> Message:
        """
        Handles user input during the CHANGES state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_show_summary(self, content: str) -> Message:
        """
        Handles user input during the SHOW_SUMMARY state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            new_state_string = self.__spot_keywords_for_new_state(content)
            new_state = get_state(new_state_string)
            if new_state == State.SAVE_SUMMARY:
                self.__saved_summary_id = self.__save_current_summary()
            return self.__switch_state_and_respond(new_state)
        except IOError:
            self.__switch_state(State.SHOW_SUMMARY)
            error_message = 'Your summary could not be saved. I apologise for your trouble, do you want to try again?'
            return self.__build_response(error_message)

    def __handle_save_summary(self) -> Message:
        """
        Handles user input during the SAVE_SUMMARY state.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        return self.__switch_state_and_respond(State.RESTART)

    def __handle_exit(self, content: str) -> Message:
        """
        Handles user input during the EXIT state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_unknown_state(self) -> Message:
        """
        Handles user input during an unknown state.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        error_message = 'Something has gone wrong. I apologize for your trouble. Please restart the chat.'
        return self.__build_response(error_message)

    def __response_without_functionality(self, content: str) -> Message:
        """
        Handles user input with no specific functionality in the current state.

        Args:
            content (str): User input message content.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        try:
            new_state_string = self.__spot_keywords_for_new_state(content)
            new_state = get_state(new_state_string)
            return self.__switch_state_and_respond(new_state)
        except NoKeywordFoundException:
            return self.__random_fallback_response()
        except NoMatchingStateException:
            # TODO log
            return self.__random_fallback_response()

    def __spot_keywords_for_new_state(self, content: str) -> str:
        """
        Identifies keywords in user input to transition to a new state.

        Args:
            content (str): User input message content.

        Returns:
            str: Keyword identified for state transition.

        Raises:
            NoKeywordFoundException: If no keyword is found in the user input.
        """
        current_transitions: Dict[str, str] = self.__transitions[self.__state.value]
        current_keywords = current_transitions.keys()
        for keyword in current_keywords:
            if keyword in content:
                return current_transitions[keyword]
        raise NoKeywordFoundException()

    def __switch_state_and_respond(self, state: State) -> Message:
        """
        Switches to a new state and responds with a message.

        Args:
            state (State): New state to switch to.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        self.__switch_state(state)
        content = self.__random_question_of_current_state()
        return self.__build_response(content)

    def __switch_to_previous_and_respond(self) -> Message:
        """
        Switches back to the previous state and responds with a message.

        Returns:
            Message: Bot message containing the response to the user input.
        """
        self.__switch_state(self.__previous_state)
        content = self.__random_question_of_current_state()
        return self.__build_response(content)

    def __switch_state(self, state: State) -> None:
        """
        Switches to a new state.

        Args:
            state (State): New state to switch to.
        """
        self.__previous_state = self.__state
        self.__state = state

    def __random_question_of_current_state(self) -> str:
        """
        Selects a random question based on the current state.

        Returns:
            str: Randomly selected question.
        """
        state_value = self.__state.value
        questions = self.__questions[state_value]
        return random.choice(questions)

    def __random_fallback_response(self) -> Message:
        """
        Generates a random fallback response.

        Returns:
            Message: Bot message containing the fallback response.
        """
        fallback = self.__random_fallback()
        return Message(
            time_sent=datetime.now(),
            sender='bot',
            content=fallback,
            is_bot_message=True
        )

    def __random_fallback(self) -> str:
        """
        Selects a random fallback message.

        Returns:
            str: Randomly selected fallback message.
        """
        return random.choice(self.__fallbacks)

    def __update_saved_summaries(self) -> None:
        """
        Updates the list of saved summary IDs.
        """
        self.__saved_summaries = saved_summary_ids()

    def __save_current_summary(self) -> int:
        """
        Saves the current summary data and returns the ID of the saved summary.

        Returns:
            int: ID of the saved summary.
        """
        summary_data = self.__summary_builder.get_summary_data()
        return save_json(summary_data)

    def __build_response(self, content: str) -> Message:
        """
        Builds a bot message response.

        Args:
            content (str): Content of the response message.

        Returns:
            Message: Bot message containing the response.
        """
        if self.__additional_info_necessary():
            content = self.__add_info(content)
        return Message(
            time_sent=datetime.now(),
            sender='bot',
            content=content,
            is_bot_message=True
        )

    def __additional_info_necessary(self) -> bool:
        """
        Checks if additional information is necessary based on the current and previous states.

        Returns:
            bool: True if additional information is necessary, False otherwise.
        """
        return (self.__state in self.__needs_additional_info
                or self.__previous_state.value.lower().startswith('input'))

    def __add_info(self, content: str) -> str:
        """
        Adds additional information to the response based on the current state.

        Args:
            content (str): Current content of the response message.

        Returns:
            str: Content of the response message with additional information added.
        """
        match self.__state:
            case State.SUMMARY_OVERVIEW:
                return self.__add_summary_overview(content)
            case State.SHOW_LOADED_SUMMARY:
                return self.__add_loaded_summary(content)
            case State.ASK_FOR_CHANGES:
                return self.__add_entered_data(content)
            case State.SHOW_SUMMARY:
                return self.__add_summary(content)
            case State.SAVE_SUMMARY:
                return self.__add_saved_summary_id(content)
            case _:
                return self.__add_info_for_saved_data(content)

    def __add_info_for_saved_data(self, content: str) -> str:
        """
        Adds additional information to the response based on the previous state.

        Args:
            content (str): Current content of the response message.

        Returns:
            str: Content of the response message with additional information added.
        """
        additional_info = ''
        match self.__previous_state:
            case State.INPUT_STARTDATE:
                additional_info = self.__summary_data.get_start_date().strftime("%d.%m.%Y")
            case State.INPUT_MONTHS:
                additional_info = f'{self.__summary_data.get_months()} months'
            case State.INPUT_KM_LIMIT:
                additional_info = f'{self.__summary_data.get_km_limit()} km'
            case State.INPUT_KM_DRIVEN:
                additional_info = f'{self.__summary_data.get_km_driven()} km'
        if additional_info:
            return f'I saved: {additional_info}.\n{content}'
        else:
            return content

    def __add_summary_overview(self, content: str) -> str:
        """
        Adds additional information to the response for the SUMMARY_OVERVIEW state.

        Args:
            content (str): Current content of the response message.

        Returns:
            str: Content of the response message with additional information added.
        """
        self.__update_saved_summaries()
        if self.__saved_summaries:
            formatted_numbers = ', '.join(str(num) for num in sorted(self.__saved_summaries))
            return f'{content}\n{formatted_numbers}\nPlease choose one.'
        else:
            self.__switch_state(State.START)
            return 'Unfortunately, there are no saved summaries. Do you wanna start over?'

    def __add_loaded_summary(self, content: str) -> str:
        """
        Adds additional information to the response for the SHOW_LOADED_SUMMARY state.

        Args:
            content (str): Current content of the response message.

        Returns:
            str: Content of the response message with additional information added.
        """
        self.__update_saved_summaries()
        if self.__loaded_summary_id in self.__saved_summaries:
            summary_data = read_summary_with_id(self.__loaded_summary_id)
            summary = SummaryBuilder.get_summary_from_data(summary_data)
            return f'{content}\n\n{summary}\n\nDo you want to load another summary?'
        else:
            self.__switch_state(State.SUMMARY_OVERVIEW)
            return 'This id is invalid. Please provide a different id.'

    def __add_entered_data(self, content: str) -> str:
        """
        Adds entered data information to the response for the ASK_FOR_CHANGES state.

        Args:
            content (str): Current content of the response message.

        Returns:
            str: Content of the response message with entered data information added.
        """
        entered_data = str(self.__summary_data)
        return f'{content}\n\n{entered_data}'

    def __add_summary(self, content: str) -> str:
        """
        Adds summary information to the response for the SHOW_SUMMARY state.

        Args:
            content (str): Current content of the response message.

        Returns:
            str: Content of the response message with summary information added.
        """
        if self.__summary_data.is_complete():
            self.__build_summary_builder()
            summary = self.__summary_builder.get_summary()
            return f'{content}\n\n{summary}\n\nDo you want to save your summary?'
        else:
            self.__switch_state(State.ASK_FOR_CHANGES)
            return f'Summary cannot be built because some values are missing. Do you want to enter the missing values?'

    def __add_saved_summary_id(self, content: str) -> str:
        """
        Adds saved summary ID information to the response for the SAVE_SUMMARY state.

        Args:
            content (str): Current content of the response message.

        Returns:
            str: Content of the response message with saved summary ID information added.
        """
        return f'{content} {self.__saved_summary_id}'

    def __build_summary_builder(self) -> None:
        """
        Builds the summary builder object using summary data.
        """
        start_data = self.__summary_data.get_start_date()
        months = self.__summary_data.get_months()
        km_limit = self.__summary_data.get_km_limit()
        km_driven = self.__summary_data.get_km_driven()
        self.__summary_builder = SummaryBuilder(start_data, months, km_limit, km_driven)


# to test the bot without the frontend (in the console)
if __name__ == '__main__':
    bot = Bot()
    user = User(name='klaus')


    def get_answer_to(msg):
        message = Message(
            time_sent=datetime.now(),
            sender=user.name,
            content=msg,
            is_bot_message=False
        )
        response = bot.respond_to(message)
        print(response.content)


    print(bot.get_start_message().content)
    while True:
        msg = input('You: ')
        get_answer_to(msg)
