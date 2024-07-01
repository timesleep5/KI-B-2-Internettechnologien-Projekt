import logging
import random
from datetime import datetime
from typing import List, Dict

from SummaryBuilder import SummaryBuilder
from datastructures.ChatModels import Message, User
from datastructures.States import State, get_state
from datastructures.SummaryData import SummaryData
from utils.Exceptions import NoKeywordFoundException, NoMatchingStateException
from utils.format_utils import is_valid_startdate, is_strictly_positive_integer, is_positive_integer
from utils.fs_utils import read_json, Paths, saved_summary_ids, \
    save_json, read_summary_with_id
from utils.regex_utils import find_number, find_date, find_summary_id


class Bot:
    """
    Represents a chatbot that interacts with users to manage leasing summaries.

    Attributes:
        __logger (Logger): Logs critical errors.
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
        __current_message (str): The content of the currently built message.
    """

    def __init__(self):
        """
        Initializes a Bot instance, setting up initial states, loading JSON data,
        and preparing necessary attributes.
        """
        logging.basicConfig(filename='logs/bot.log')
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.INFO)

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

        self.__current_message: str

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

        :return: Bot message containing the greeting.
        """
        self.__current_message = random.choice(self.__greetings)
        return self.__build_response()

    def get_start_message(self) -> Message:
        """
        Generates the initial message when starting the conversation.

        :return: Bot message containing the start message.
        """
        self.__current_message = self.__random_question_of_current_state()
        return self.__build_response()

    def respond_to(self, message: Message) -> Message:
        """
        Responds to the user message based on the current state.

        :param message: User message containing the user input.
        :return: Bot message containing the response to the user input.
        """
        self.__current_message = ''
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

        :param content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        self.__update_saved_summaries()
        new_state_string = ''
        try:
            new_state_string = self.__spot_keywords_for_new_state(content)
            new_state = get_state(new_state_string)
            if new_state == State.LOAD_SUMMARY and not self.__saved_summaries:
                return self.__switch_state_and_respond(State.INPUT_STARTDATE)
            return self.__switch_state_and_respond(new_state)
        except NoKeywordFoundException:
            return self.__random_fallback_response()
        except NoMatchingStateException:
            self.__logger.critical(f'Unknown state: {new_state_string}')
            return self.__random_fallback_response()

    def __handle_restart(self, content: str) -> Message:
        """
        Handles user input during the RESTART state.

        :param content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        new_state_string = ''
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
            self.__logger.critical(f'Unknown state: {new_state_string}')
            return self.__random_fallback_response()

    def __handle_help(self) -> Message:
        """
        Handles user input during the HELP state.

        :return: Bot message containing the response to the user input.
        """
        return self.__switch_to_previous_and_respond()

    def __handle_load_summary(self, content: str) -> Message:
        """
        Handles user input during the LOAD_SUMMARY state.

        :param content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_summary_overview(self, content: str) -> Message:
        """
        Handles user input during the SUMMARY_OVERVIEW state.

        :param content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        try:
            self.__loaded_summary_id = find_summary_id(content)
            return self.__switch_state_and_respond(State.SHOW_LOADED_SUMMARY)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_show_loaded_summary(self, content: str) -> Message:
        """
        Handles user input during the SHOW_LOADED_SUMMARY state.

        :param content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_input_startdate(self, content: str) -> Message:
        """
        Handles user input during the INPUT_STARTDATE state.

        :param content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        try:
            startdate = find_date(content)
            if not is_valid_startdate(startdate):
                self.__current_message += ('You have to enter a startdate that lies at least one day in the past.\n'
                                           'The summary only works for contracts that are already running.\n'
                                           f'{self.__random_question_of_current_state()}')
                return self.__build_response()
            self.__summary_data.set_start_date(startdate)
            self.__add_saved_startdate_to_message()
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_MONTHS)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_input_months(self, content: str) -> Message:
        """
        Handles user input during the INPUT_MONTHS state.

        :param content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        try:
            months = find_number(content)
            if not is_strictly_positive_integer(months):
                self.__current_message += ('You must enter a strictly positive number as a runtime of months.\n'
                                           'That means, the number must be greater than zero.\n'
                                           f'{self.__random_question_of_current_state()}')
                return self.__build_response()
            self.__summary_data.set_months(months)
            self.__add_saved_months_to_message()
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_KM_LIMIT)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_input_km_limit(self, content: str) -> Message:
        """
        Handles user input during the INPUT_KM_LIMIT state.

        :param  content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        try:
            km_limit = find_number(content)
            if not is_strictly_positive_integer(km_limit):
                self.__current_message += ('You must enter a strictly positive number as a kilometer limit.\n'
                                           'That means, the number must be greater than zero.\n'
                                           f'{self.__random_question_of_current_state()}')
                return self.__build_response()
            self.__summary_data.set_km_limit(km_limit)
            self.__add_saved_km_limit_to_message()
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_KM_DRIVEN)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_input_km_driven(self, content: str) -> Message:
        """
        Handles user input during the INPUT_KM_DRIVEN state.

        :param  content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        try:
            km_driven = find_number(content)
            if not is_positive_integer(km_driven):
                self.__current_message += ('You must enter a positive number as a runtime of months.\n'
                                           'That means, the number must be greater than or equal to zero.\n'
                                           f'{self.__random_question_of_current_state()}')
                return self.__build_response()
            self.__summary_data.set_km_driven(km_driven)
            self.__add_saved_km_driven_to_message()
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.ASK_FOR_CHANGES)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_ask_for_changes(self, content: str) -> Message:
        """
        Handles user input during the ASK_FOR_CHANGES state.

        :param  content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_changes(self, content: str) -> Message:
        """
        Handles user input during the CHANGES state.

        :param  content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_show_summary(self, content: str) -> Message:
        """
        Handles user input during the SHOW_SUMMARY state.

        :param  content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        try:
            new_state_string = self.__spot_keywords_for_new_state(content)
            new_state = get_state(new_state_string)
            if new_state == State.SAVE_SUMMARY:
                self.__saved_summary_id = self.__save_current_summary()
            return self.__switch_state_and_respond(new_state)
        except IOError:
            self.__switch_state(State.SHOW_SUMMARY)
            self.__current_message = 'Your summary could not be saved. I apologise for your trouble, do you want to try again?'
            return self.__build_response()

    def __handle_save_summary(self) -> Message:
        """
        Handles user input during the SAVE_SUMMARY state.

        :return: Bot message containing the response to the user input.
        """
        return self.__switch_state_and_respond(State.RESTART)

    def __handle_exit(self, content: str) -> Message:
        """
        Handles user input during the EXIT state.

        :param  content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        return self.__response_without_functionality(content)

    def __handle_unknown_state(self) -> Message:
        """
        Handles user input during an unknown state.

        :return: Bot message containing the response to the user input.
        """
        self.__current_message = 'Something has gone wrong. I apologize for your trouble. Please restart the chat.'
        return self.__build_response()

    def __response_without_functionality(self, content: str) -> Message:
        """
        Handles user input with no specific functionality in the current state.

        :param  content: User input message content.
        :return: Bot message containing the response to the user input.
        """
        new_state_string = ''
        try:
            new_state_string = self.__spot_keywords_for_new_state(content)
            new_state = get_state(new_state_string)
            return self.__switch_state_and_respond(new_state)
        except NoKeywordFoundException:
            return self.__random_fallback_response()
        except NoMatchingStateException:
            self.__logger.critical(f'Unknown state: {new_state_string}')
            return self.__random_fallback_response()

    def __spot_keywords_for_new_state(self, content: str) -> str:
        """
        Identifies keywords in user input to transition to a new state.

        :param  content: User input message content.
        :return: Keyword identified for state transition.
        :raise NoKeywordFoundException: If no keyword is found in the user input.
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

        :param  state (State): New state to switch to.
        :return: Bot message containing the response to the user input.
        """
        self.__switch_state(state)
        self.__current_message += self.__random_question_of_current_state()
        if self.__additional_info_necessary():
            self.__add_info()
        return self.__build_response()

    def __switch_to_previous_and_respond(self) -> Message:
        """
        Switches back to the previous state and responds with a message.

        :return: Bot message containing the response to the user input.
        """
        return self.__switch_state_and_respond(self.__previous_state)

    def __switch_state(self, state: State) -> None:
        """
        Switches to a new state.

        :param  state: New state to switch to.
        """
        self.__previous_state = self.__state
        self.__state = state

    def __random_question_of_current_state(self) -> str:
        """
        Selects a random question based on the current state.

        :return: Randomly selected question.
        """
        state_value = self.__state.value
        questions = self.__questions[state_value]
        return random.choice(questions)

    def __random_fallback_response(self) -> Message:
        """
        Generates a random fallback response.

        :return: Bot message containing the fallback response.
        """
        self.__current_message += self.__random_fallback()
        return Message(
            time_sent=datetime.now(),
            sender='bot',
            content=self.__current_message,
            is_bot_message=True
        )

    def __random_fallback(self) -> str:
        """
        Selects a random fallback message.

        :return: Randomly selected fallback message.
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

        :return: ID of the saved summary.
        """
        summary_data = self.__summary_builder.get_summary_data()
        return save_json(summary_data)

    def __build_response(self) -> Message:
        """
        Builds a bot message response.

        :return: Bot message containing the response.
        """
        return Message(
            time_sent=datetime.now(),
            sender='bot',
            content=self.__current_message,
            is_bot_message=True
        )

    def __additional_info_necessary(self) -> bool:
        """
        Checks if additional information is necessary based on the current and previous states.

        :return: True if additional information is necessary, False otherwise.
        """
        return self.__state in self.__needs_additional_info

    def __add_info(self) -> None:
        """
        Adds additional information to the response based on the current state.
        """
        match self.__state:
            case State.SUMMARY_OVERVIEW:
                self.__add_summary_overview()
            case State.SHOW_LOADED_SUMMARY:
                self.__add_loaded_summary()
            case State.ASK_FOR_CHANGES:
                self.__add_entered_data()
            case State.SHOW_SUMMARY:
                self.__add_summary()
            case State.SAVE_SUMMARY:
                self.__add_saved_summary_id()
            case _:
                self.__logger.critical(f'state should not require additional info: {self.__state}')

    def __add_summary_overview(self) -> None:
        """
        Adds additional information to the response for the SUMMARY_OVERVIEW state.
        """
        self.__update_saved_summaries()
        if self.__saved_summaries:
            formatted_numbers = ', '.join(str(num) for num in sorted(self.__saved_summaries))
            self.__current_message += f'\n{formatted_numbers}\nPlease choose one.'
        else:
            self.__switch_state(State.START)
            self.__current_message = 'Unfortunately, there are no saved summaries. Do you wanna start over?'

    def __add_loaded_summary(self) -> None:
        """
        Adds additional information to the response for the SHOW_LOADED_SUMMARY state.
        """
        self.__update_saved_summaries()
        if self.__loaded_summary_id in self.__saved_summaries:
            summary_data = read_summary_with_id(self.__loaded_summary_id)
            summary = SummaryBuilder.get_summary_from_data(summary_data)
            self.__current_message += f'\n\n{summary}\n\nDo you want to load another summary?'
        else:
            self.__switch_state(State.SUMMARY_OVERVIEW)
            self.__current_message = 'This id is invalid. Please provide a different id.'

    def __add_entered_data(self) -> None:
        """
        Adds entered data information to the response for the ASK_FOR_CHANGES state.
        """
        entered_data = str(self.__summary_data)
        self.__current_message += f'\n\n{entered_data}\n\nDo you need to modify any details in your contract?'

    def __add_summary(self) -> None:
        """
        Adds summary information to the response for the SHOW_SUMMARY state.
        """
        if self.__summary_data.is_complete():
            self.__build_summary_builder()
            summary = self.__summary_builder.get_summary()
            self.__current_message += f'\n\n{summary}\n\nDo you want to save your summary?'
        else:
            self.__switch_state(State.ASK_FOR_CHANGES)
            self.__current_message = ('Summary cannot be built because some values are missing. '
                                      'Do you want to enter the missing values?')

    def __add_saved_summary_id(self) -> None:
        """
        Adds saved summary ID information to the response for the SAVE_SUMMARY state.
        """
        self.__current_message += f' {self.__saved_summary_id}'

    def __add_saved_startdate_to_message(self) -> None:
        """
        Adds the saved start date information to the current message.

        The start date is formatted as "dd.mm.yyyy" and appended to the current message.
        """
        additional_info = self.__summary_data.get_start_date().strftime("%d.%m.%Y")
        self.__add_saved_data_message(additional_info)

    def __add_saved_months_to_message(self) -> None:
        """
        Adds the saved number of months information to the current message.

        The number of months is appended to the current message, with proper pluralization.
        """
        number_of_months = self.__summary_data.get_months()
        additional_info = f'{number_of_months} month{"s" if number_of_months != 1 else ""}'
        self.__add_saved_data_message(additional_info)

    def __add_saved_km_limit_to_message(self) -> None:
        """
        Adds the saved kilometer limit information to the current message.

        The kilometer limit is appended to the current message.
        """
        additional_info = f'{self.__summary_data.get_km_limit()} km'
        self.__add_saved_data_message(additional_info)

    def __add_saved_km_driven_to_message(self) -> None:
        """
        Adds the saved kilometers driven information to the current message.

        The kilometers driven is appended to the current message.
        """
        additional_info = f'{self.__summary_data.get_km_driven()} km'
        self.__add_saved_data_message(additional_info)

    def __add_saved_data_message(self, saved_data: str) -> None:
        """
        Appends saved data information to the current message.

        The saved data is prefixed with "I saved: " and appended to the current message.

        :param saved_data: The data to append to the current message.
        """
        new_message = f'I saved: {saved_data}.\n{self.__current_message}'
        self.__current_message = new_message

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
