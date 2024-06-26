import random
from datetime import datetime
from typing import List, Dict

from datastructures.ChatModels import UserMessage, BotMessage, User
from datastructures.States import State, get_state
from SummaryBuilder import SummaryBuilder
from utils.Exceptions import NoKeywordFoundException, NoMatchingStateException
from datastructures.SummaryData import SummaryData
from utils.fs_utils import read_json, Paths, saved_summary_ids, \
    save_json, read_summary_with_id
from utils.regex_utils import find_number, find_date, find_summary_id


class Bot:
    def __init__(self):
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
        self.__questions = read_json(Paths.BOT_QUESTIONS)
        self.__fallbacks = read_json(Paths.BOT_FALLBACKS)
        self.__transitions = read_json(Paths.BOT_TRANSITIONS)
        self.__greetings = read_json(Paths.BOT_GREETINGS)

    def get_greeting(self) -> BotMessage:
        message = random.choice(self.__greetings)
        return self.__build_response(message)

    def get_start_message(self) -> BotMessage:
        message = self.__random_question_of_current_state()
        return self.__build_response(message)

    def respond_to(self, message: UserMessage) -> BotMessage:
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

    def __handle_start(self, content: str) -> BotMessage:
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

    def __handle_restart(self, content: str) -> BotMessage:
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

    def __handle_help(self) -> BotMessage:
        return self.__switch_to_previous_and_respond()

    def __handle_load_summary(self, content: str) -> BotMessage:
        return self.__response_without_functionality(content)

    def __handle_summary_overview(self, content: str) -> BotMessage:
        try:
            self.__loaded_summary_id = find_summary_id(content)
            return self.__switch_state_and_respond(State.SHOW_LOADED_SUMMARY)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_show_loaded_summary(self, content: str) -> BotMessage:
        return self.__response_without_functionality(content)

    def __handle_input_startdate(self, content: str) -> BotMessage:
        try:
            startdate = find_date(content)
            self.__summary_data.set_start_date(startdate)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_MONTHS)
        except ValueError:
            return self.__response_without_functionality(content)

    def __handle_input_months(self, content: str) -> BotMessage:
        try:
            months = find_number(content)
            self.__summary_data.set_months(months)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_KM_LIMIT)
        except ValueError:
            self.__response_without_functionality(content)

    def __handle_input_km_limit(self, content: str) -> BotMessage:
        try:
            km_limit = find_number(content)
            self.__summary_data.set_km_limit(km_limit)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.INPUT_KM_DRIVEN)
        except ValueError:
            self.__response_without_functionality(content)

    def __handle_input_km_driven(self, content: str) -> BotMessage:
        try:
            km_driven = find_number(content)
            self.__summary_data.set_km_driven(km_driven)
            if self.__previous_state == State.CHANGES:
                return self.__switch_state_and_respond(self.__previous_state)
            return self.__switch_state_and_respond(State.ASK_FOR_CHANGES)
        except ValueError:
            self.__response_without_functionality(content)

    def __handle_ask_for_changes(self, content: str) -> BotMessage:
        return self.__response_without_functionality(content)

    def __handle_changes(self, content: str) -> BotMessage:
        return self.__response_without_functionality(content)

    def __handle_show_summary(self, content: str) -> BotMessage:
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

    def __handle_save_summary(self) -> BotMessage:
        return self.__switch_state_and_respond(State.RESTART)

    def __handle_exit(self, content: str) -> BotMessage:
        return self.__response_without_functionality(content)

    def __handle_unknown_state(self) -> BotMessage:
        error_message = 'Something has gone wrong. I apologize for your trouble. Please restart the chat.'
        return self.__build_response(error_message)

    def __response_without_functionality(self, content: str) -> BotMessage:
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
        current_transitions: Dict[str, str] = self.__transitions[self.__state.value]
        current_keywords = current_transitions.keys()
        for keyword in current_keywords:
            if keyword in content:
                return current_transitions[keyword]
        raise NoKeywordFoundException()

    def __switch_state_and_respond(self, state: State) -> BotMessage:
        self.__switch_state(state)
        content = self.__random_question_of_current_state()
        return self.__build_response(content)

    def __switch_to_previous_and_respond(self) -> BotMessage:
        self.__switch_state(self.__previous_state)
        content = self.__random_question_of_current_state()
        return self.__build_response(content)

    def __switch_state(self, state: State) -> None:
        self.__previous_state = self.__state
        self.__state = state

    def __random_question_of_current_state(self) -> str:
        state_value = self.__state.value
        questions = self.__questions[state_value]
        return random.choice(questions)

    def __random_fallback_response(self) -> BotMessage:
        fallback = self.__random_fallback()
        return BotMessage(
            time_sent=datetime.now(),
            content=fallback
        )

    def __random_fallback(self) -> str:
        return random.choice(self.__fallbacks)

    def __update_saved_summaries(self) -> None:
        self.__saved_summaries = saved_summary_ids()

    def __save_current_summary(self) -> int:
        summary_data = self.__summary_builder.get_summary_data()
        return save_json(summary_data)

    def __build_response(self, content: str) -> BotMessage:
        if self.__additional_info_necessary():
            content = self.__add_info(content)
        return BotMessage(
            time_sent=datetime.now(),
            content=content
        )

    def __additional_info_necessary(self) -> bool:
        return (self.__state in self.__needs_additional_info
                or self.__previous_state.value.lower().startswith('input'))

    def __add_info(self, content: str) -> str:
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
        self.__update_saved_summaries()
        if self.__saved_summaries:
            formatted_numbers = ', '.join(str(num) for num in sorted(self.__saved_summaries))
            return f'{content}\n{formatted_numbers}\nPlease choose one.'
        else:
            self.__switch_state(State.START)
            return 'Unfortunately, there are no saved summaries. Do you wanna start over?'

    def __add_loaded_summary(self, content: str) -> str:
        self.__update_saved_summaries()
        if self.__loaded_summary_id in self.__saved_summaries:
            summary_data = read_summary_with_id(self.__loaded_summary_id)
            summary = SummaryBuilder.get_summary_from_data(summary_data)
            return f'{content}\n\n{summary}\n\nDo you want to load another summary?'
        else:
            self.__switch_state(State.SUMMARY_OVERVIEW)
            return 'This id is invalid. Please provide a different id.'

    def __add_entered_data(self, content: str) -> str:
        entered_data = str(self.__summary_data)
        return f'{content}\n\n{entered_data}'

    def __add_summary(self, content: str) -> str:
        if self.__summary_data.is_complete():
            self.__build_summary_builder()
            summary = self.__summary_builder.get_summary()
            return f'{content}\n\n{summary}\n\nDo you want to save your summary?'
        else:
            self.__switch_state(State.ASK_FOR_CHANGES)
            return f'Summary cannot be built because some values are missing. Do you want to enter the missing values?'

    def __add_saved_summary_id(self, content: str) -> str:
        return f'{content} {self.__saved_summary_id}'

    def __build_summary_builder(self) -> None:
        start_data = self.__summary_data.get_start_date()
        months = self.__summary_data.get_months()
        km_limit = self.__summary_data.get_km_limit()
        km_driven = self.__summary_data.get_km_driven()
        self.__summary_builder = SummaryBuilder(start_data, months, km_limit, km_driven)


if __name__ == '__main__':
    bot = Bot()
    user = User(name='klaus')


    def get_answer_to(msg):
        message = UserMessage(id=1, time_sent=datetime.now(), content=msg, user=user)
        response = bot.respond_to(message)
        print(response.content)


    print(bot.get_start_message().content)
    while True:
        msg = input('You: ')
        get_answer_to(msg)
