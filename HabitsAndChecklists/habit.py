from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod, DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence, YearlyRecurrence, OnceRecurrence, DaysOfMonthKRecurrence, NthWeekdayMOfMonthKRecurrence, AggregateRecurrence
import datetime as dt
from DataObjectConversion.textEquivalent import TextEquivalent
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput
from DataObjectConversion.dataStack import DataStack



class Habit(TextEquivalent):
    def __init__(self, title: str, required: bool, upcomingBuffer: int, recurrence: Recurrence, doneByTimes: list[dt.time]):
        self.title = title
        self.required = required
        self.upcomingBuffer = upcomingBuffer
        self.recurrence = recurrence
        self.doneByTimes = doneByTimes


    @staticmethod
    def setupPrompt(indent: int=0):
        UserOutput.indentedPrint("habit", indent)
        title = UserInput.getStringInput("habit title? ", indent=indent+1)
        required = UserInput.getBoolInput("required? ", indent=indent+1)
        upcomingBuffer = UserInput.getIntInput("notify how many days in advance? ", indent=indent+1)
        recurrence = Recurrence.setupPrompt(indent=indent+1)
        doneByTimes = None
        habit = Habit(title, required, upcomingBuffer, recurrence, doneByTimes)
        habit.savePrompt(indent=indent+1)
        return habit


    def savePrompt(self, indent: int=0):
        save = UserInput.getBoolInput("save this habit? ", indent=indent)
        if save:
            name = UserInput.getStringInput("what would you like to save this habit as? ", indent=indent+1)
            DataStack.addHabit(self, name)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()):
        return self.recurrence.nextOccurrence(referenceDate=referenceDate)


    def isUpcoming(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        if nextOcc == None: return False
        return referenceDate + dt.timedelta(days=self.upcomingBuffer) >= nextOcc


    def toText(self, indent: int=0):
        text = f"habit: {self.title}\n"
        text += f"{UserOutput.indentStyle}required: {self.required}\n"
        text += f"{UserOutput.indentStyle}upcoming buffer: {self.upcomingBuffer} days\n"
        text += self.recurrence.toText(indent=1)
        return super().indentText(text, indent)


