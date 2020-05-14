import pygame

# Timer class for the game
# We count time every second, an the time elapsed in game is 60 times the actual time
# So, if we spend 60 seconds, we count that we spent 60 minutes.

# Day/night cycle parameters
DAY_START = "7:00"
NIGHT_START = "22:00"


class Timer:
    def __init__(self, startTime="12:00"):
        """
        Create an in-game timer. It acts like a regular clock, but each minute is one second IRL.
        The clock is not started by default. Call Timer.startClock() to make it running.

        :param startTime: Starting time as a string in the format of HH:MM, where HH is hours value, MM is minutes value
        """
        self.clock = pygame.time.Clock()

        # Time in milliseconds updated every frame, starts counting from what we specify as a parameter
        self.timePassed = self.timeToMs(startTime)
        # You have to start the clock manually by calling startClock() method
        self.isStarted = False

    def startClock(self):
        """
        Start the clock.
        """
        self.isStarted = True

    def stopClock(self):
        """
        Stop the clock.
        """
        self.isStarted = False

    def getPrettyTime(self):
        """
        Get a pretty looking time.

        :return: String in the format of HH:MM
        """
        # 60 times faster than real time
        minutes = int(self.timePassed / 1000) % 60
        hours = int(self.timePassed / 60000) % 24

        # Add 0's at the beginning if necessary
        prefixHr = ""
        prefixMin = ""
        if len(str(hours)) < 2:
            prefixHr = "0"
        if len(str(minutes)) < 2:
            prefixMin = "0"

        # Return a formatted time
        return prefixHr + str(hours) + ":" + prefixMin + str(minutes)

    def isItDay(self):
        """
        Get current cycle.

        :return: True, if it's daytime, otherwise False.
        """
        if self.timeToMs(DAY_START) < self.timePassed < self.timeToMs(NIGHT_START):
            return True
        else:
            return False

    def updateTime(self, elapsed):
        """
        Should be called every frame to update the timer.

        :param elapsed: Time of the frame
        """
        # Only happens if the time is set to be running
        if self.isStarted:
            # Modulo, since we use the 24-hour cycle
            # In our case, the time loops every 24 minutes
            self.timePassed = (self.timePassed + elapsed) % 1440000

    def timeToMs(self, timeString):
        """
        Converts time from string format to milliseconds.

        :param timeString: Time string in format HH:MM
        :return: Milliseconds integer
        """
        timeList = timeString.split(':')
        hours = timeList[0]
        minutes = timeList[1]
        return int(hours) * 60000 + int(minutes) * 1000
