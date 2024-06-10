from datetime import datetime
from enum import Enum
from textwrap import dedent
from typing import List

from SummaryBuilder import SummaryBuilder
from ChatModels import UserMessage, BotMessage, User


class BotAction(Enum):
    NO_IDEA = 'no idea'
    NO_CALCULATOR = 'no calculator'

    HELP = 'help'

    SET_START_DATE = 'set the start date for the contract'
    SET_RUNTIME_MONTHS = 'set the runtime in months for the contract'
    SET_KM_LIMIT = 'set the km limit for the contract'
    SET_KM_DRIVEN = 'set the driven kilometers'

    GET_SUMMARY = 'summary'


class KeywordList:
    def __init__(self, keywords: List[str]):
        self.keywords = keywords


keywords_to_actions = {
    KeywordList(['help', 'clueless', 'instructions', 'handbook']): BotAction.HELP,

    KeywordList(['start', 'date']): BotAction.SET_START_DATE,
    KeywordList(['runtime', 'months']): BotAction.SET_RUNTIME_MONTHS,
    KeywordList(['km_limit']): BotAction.SET_KM_LIMIT,
    KeywordList(['drove', 'km_driven']): BotAction.SET_KM_DRIVEN,

    KeywordList(['summary', 'overview']): BotAction.GET_SUMMARY,
}


class StringManipulation:
    @staticmethod
    def to_words(content: str) -> List[str]:
        separators = [',', '.', ':', '?', '!']
        before = content.split()
        after = []
        for separator in separators:
            for word in before:
                after += word.split(separator)
            before, after = after, []
        return list(filter(lambda word: word != '', before))

    @staticmethod
    def get_value_string(content: str) -> str:
        separator = ':'
        after_separator = content.split(separator)[-1].strip()
        value_string = StringManipulation.to_words(after_separator)[0]
        return value_string


class Bot:
    def __init__(self):
        self.__summary_builder = None
        self.__start_date = None
        self.__runtime_months = None
        self.__km_limit = None
        self.__km_driven = None

    def respond_to(self, message: UserMessage) -> BotMessage:
        content = message.content
        message_for_action: str
        try:
            action_to_take = self.__derive_action_from_content(content)
            message_for_action = self.__act(action_to_take, content)
        except Exception as e:
            message_for_action = BotAction.NO_IDEA.value
        response_content = self.__build_response_content(message_for_action)
        return self.__build_response(response_content)

    def __derive_action_from_content(self, content: str) -> BotAction:
        words = StringManipulation.to_words(content)
        print('\n\n')
        print(words)
        for word in words:
            for keyword_list in keywords_to_actions.keys():
                for keyword in keyword_list.keywords:
                    if word.lower() in keyword:
                        return self.__change_action_if_original_not_viable(keywords_to_actions[keyword_list])
        return BotAction.NO_IDEA

    def __change_action_if_original_not_viable(self, action: BotAction) -> BotAction:
        requires_calculator = action == BotAction.GET_SUMMARY
        if requires_calculator and not self.__summary_builder:
            return BotAction.NO_CALCULATOR
        else:
            return action

    def __act(self, action_to_take: BotAction, content: str) -> str:
        value_string = StringManipulation.get_value_string(content)
        match action_to_take:
            case BotAction.SET_START_DATE:
                self.__start_date = datetime.strptime(value_string, '%d-%m-%Y')
            case BotAction.SET_RUNTIME_MONTHS:
                self.__runtime_months = int(value_string)
            case BotAction.SET_KM_LIMIT:
                self.__km_limit = int(value_string)
            case BotAction.SET_KM_DRIVEN:
                self.__km_driven = int(value_string)
        self.__build_summary_builder_if_possible()

        return str(action_to_take.value)

    def __build_response_content(self, message_for_action: str) -> str:
        if message_for_action.startswith('set'):
            return f'Thanks for your input! I {message_for_action}. If you need anything else, let me know.'
        elif message_for_action.startswith('summary'):
            return f'Here is your summary: \n{self.__summary_builder.get_summary()}'
        elif message_for_action.startswith('no calculator'):
            return ('I understand what you want from me, but I\'m sorry, I can\'t give you that.\n'
                    f'Unfortunately, there is still some missing data from your contract:\n'
                    + self.__list_of_missing_variables())
        elif message_for_action.startswith('help'):
            return dedent("""
            Hi, I'm here to help you calculate everything in your leasing contract of BMW or MINI.
            Just give me the most important pieces data of your contract, and we can start! 
            These pieces are: 
              - The start date of the contract in the format 'DD-MM-YYYY' (date)
              - The runtime of your contract in months (months)
              - The kilometer limit of your contract (limit)
              - The kilometers you already drove so far (driven)
            
            For me to understand you better, I should mention a few things:
            I'm not the brightest, so you have to keep a simple syntax if you want to set the data. 
            It should be of the following format: 
                [keyword, you can use the ones in the braces above]: [value without unit]
            Alright, that would be all. Let's start!""")
        else:
            return 'I\'m sorry, I have no idea what you are talking about.'

    def __list_of_missing_variables(self) -> str:
        missing_variables = []
        if self.__start_date is None:
            missing_variables.append('start date')
        if self.__runtime_months is None:
            missing_variables.append('runtime in months')
        if self.__km_limit is None:
            missing_variables.append('the kilometer limit')
        if self.__km_driven is None:
            missing_variables.append('the kilometer you drove')
        return ', '.join(missing_variables)

    def __build_response(self, content: str) -> BotMessage:
        return BotMessage(
            time_sent=datetime.now(),
            content=content
        )

    def __build_summary_builder_if_possible(self) -> None:
        if self.__summary_builder_can_be_built():
            self.__build_summary_builder()

    def __summary_builder_can_be_built(self) -> bool:
        return (self.__start_date is not None
                and self.__runtime_months is not None
                and self.__km_limit is not None
                and self.__km_driven)

    def __build_summary_builder(self) -> None:
        self.__summary_builder = SummaryBuilder(
            self.__start_date, self.__runtime_months, self.__km_limit, self.__km_driven
        )


if __name__ == '__main__':
    bot = Bot()
    user = User(name='klaus')


    def get_answer_to(msg):
        message = UserMessage(id=1, time_sent=datetime.now(), content=msg, user=user)
        response = bot.respond_to(message)
        print(response.content)


    get_answer_to('help')
    get_answer_to('driven: 2714')
    get_answer_to('date: 01-03-2024')
    get_answer_to('limit: 8000')
    get_answer_to('months: 9')
    get_answer_to('summary')
