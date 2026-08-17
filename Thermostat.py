#
# Thermostat - This is the Python code used to demonstrate
# the functionality of the thermostat that we have prototyped
# throughout the course.
#

from time import sleep
from datetime import datetime

from statemachine import StateMachine, State

import board
import adafruit_ahtx0

import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

import serial

from gpiozero import Button, PWMLED

from threading import Thread

from math import floor


DEBUG = True


# ------------------------------------------------------------
# I2C temperature sensor
# ------------------------------------------------------------

i2c = board.I2C()

thSensor = adafruit_ahtx0.AHTx0(i2c)


# ------------------------------------------------------------
# UART
# ------------------------------------------------------------

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


# ------------------------------------------------------------
# LEDs
# ------------------------------------------------------------

redLight = PWMLED(18)
blueLight = PWMLED(23)


# ------------------------------------------------------------
# LCD Display
# ------------------------------------------------------------

class ManagedDisplay():

    def __init__(self):

        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        self.lcd_columns = 16
        self.lcd_rows = 2

        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs,
            self.lcd_en,
            self.lcd_d4,
            self.lcd_d5,
            self.lcd_d6,
            self.lcd_d7,
            self.lcd_columns,
            self.lcd_rows
        )

        self.lcd.clear()

    def cleanupDisplay(self):

        self.lcd.clear()

        self.lcd_rs.deinit()
        self.lcd_en.deinit()
        self.lcd_d4.deinit()
        self.lcd_d5.deinit()
        self.lcd_d6.deinit()
        self.lcd_d7.deinit()

    def clear(self):
        self.lcd.clear()

    def updateScreen(self, message):
        self.lcd.clear()
        self.lcd.message = message


# Initialize display
screen = ManagedDisplay()


# ------------------------------------------------------------
# Thermostat State Machine
# ------------------------------------------------------------

class TemperatureMachine(StateMachine):

    "A state machine designed to manage our thermostat"

    off = State(initial=True)
    heat = State()
    cool = State()

    # Default set point
    setPoint = 72

    # State transitions
    cycle = (
        off.to(heat) |
        heat.to(cool) |
        cool.to(off)
    )

    # --------------------------------------------------------
    # Heat state
    # --------------------------------------------------------

    def on_enter_heat(self):

        blueLight.off()

        if DEBUG:
            print("* Changing state to heat")

    def on_exit_heat(self):

        redLight.off()

    # --------------------------------------------------------
    # Cool state
    # --------------------------------------------------------

    def on_enter_cool(self):

        redLight.off()

        if DEBUG:
            print("* Changing state to cool")

    def on_exit_cool(self):

        blueLight.off()

    # --------------------------------------------------------
    # Off state
    # --------------------------------------------------------

    def on_enter_off(self):

        redLight.off()
        blueLight.off()

        if DEBUG:
            print("* Changing state to off")

    # --------------------------------------------------------
    # State button
    # --------------------------------------------------------

    def processTempStateButton(self):

        if DEBUG:
            print("Cycling Temperature State")

        self.cycle()

        self.updateLights()

    # --------------------------------------------------------
    # Increase temperature
    # --------------------------------------------------------

    def processTempIncButton(self):

        if DEBUG:
            print("Increasing Set Point")

        self.setPoint += 1

        self.updateLights()

    # --------------------------------------------------------
    # Decrease temperature
    # --------------------------------------------------------

    def processTempDecButton(self):

        if DEBUG:
            print("Decreasing Set Point")

        self.setPoint -= 1

        self.updateLights()

    # --------------------------------------------------------
    # Update LEDs
    # --------------------------------------------------------

    def updateLights(self):

        temp = floor(self.getFahrenheit())

        redLight.off()
        blueLight.off()

        if DEBUG:
            print(f"State: {self.current_state.id}")
            print(f"SetPoint: {self.setPoint}")
            print(f"Temp: {temp}")

        # Thermostat OFF
        if self.current_state.id == "off":
            redLight.off()
            blueLight.off()

        # HEATING
        elif self.current_state.id == "heat":

            blueLight.off()

            # Temperature below set point:
            # red LED fades in and out
            if temp < self.setPoint:
                redLight.pulse(
                    fade_in_time=1,
                    fade_out_time=1,
                    n=None,
                    background=False
                )

            # Temperature at or above set point:
            # red LED stays solid
            else:
                redLight.on()

        # COOLING
        elif self.current_state.id == "cool":

            redLight.off()

            # Temperature above set point:
            # blue LED fades in and out
            if temp > self.setPoint:
                blueLight.pulse(
                    fade_in_time=1,
                    fade_out_time=1,
                    n=None,
                    background=False
                )

            # Temperature at or below set point:
            # blue LED stays solid
            else:
                blueLight.on()

    # --------------------------------------------------------
    # Start display thread
    # --------------------------------------------------------

    def run(self):

        myThread = Thread(target=self.manageMyDisplay)
        myThread.start()

    # --------------------------------------------------------
    # Get Fahrenheit temperature
    # --------------------------------------------------------

    def getFahrenheit(self):

        t = thSensor.temperature

        return ((9 / 5) * t) + 32

    # --------------------------------------------------------
    # UART output
    # --------------------------------------------------------

    def setupSerialOutput(self):

        state = self.current_state.id

        if state == "heat":
            state = "heat"

        elif state == "cool":
            state = "cool"

        else:
            state = "off"

        temperature = floor(self.getFahrenheit())

        output = f"{state},{temperature},{self.setPoint}\n"

        return output

    # --------------------------------------------------------
    # Display management
    # --------------------------------------------------------

    endDisplay = False

    def manageMyDisplay(self):

        counter = 1
        altCounter = 1

        while not self.endDisplay:

            if DEBUG:
                print("Processing Display Info...")

            # Get current time
            current_time = datetime.now()

            # First LCD line
            lcd_line_1 = current_time.strftime("%m/%d %H:%M:%S")

            # Keep first line within 16 characters
            lcd_line_1 = lcd_line_1[:16] + "\n"

            # Second LCD line
            if altCounter < 6:

                temperature = floor(self.getFahrenheit())

                lcd_line_2 = f"Temp: {temperature}F"

                altCounter += 1

            else:

                state = self.current_state.id

                lcd_line_2 = f"{state} Set:{self.setPoint}F"

                altCounter += 1

                if altCounter >= 11:

                    self.updateLights()

                    altCounter = 1

            # Make sure second line fits
            lcd_line_2 = lcd_line_2[:16]

            # Update LCD
            screen.updateScreen(lcd_line_1 + lcd_line_2)

            # Send UART update every 30 seconds
            if DEBUG:
                print(f"Counter: {counter}")

            if (counter % 30) == 0:

                output = self.setupSerialOutput()

                ser.write(output.encode())

                if DEBUG:
                    print(f"UART: {output.strip()}")

                counter = 1

            else:

                counter += 1

            sleep(1)

        screen.cleanupDisplay()


# ------------------------------------------------------------
# Initialize State Machine
# ------------------------------------------------------------

tsm = TemperatureMachine()

tsm.run()


# ------------------------------------------------------------
# State button - GPIO 24
# ------------------------------------------------------------

greenButton = Button(24)

greenButton.when_pressed = tsm.processTempStateButton


# ------------------------------------------------------------
# Increase button - GPIO 25
# ------------------------------------------------------------

redButton = Button(25)

redButton.when_pressed = tsm.processTempIncButton


# ------------------------------------------------------------
# Decrease button - GPIO 12
# ------------------------------------------------------------

blueButton = Button(12)

blueButton.when_pressed = tsm.processTempDecButton


# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------

repeat = True

while repeat:

    try:

        sleep(30)

    except KeyboardInterrupt:

        print("Cleaning up. Exiting...")

        repeat = False

        tsm.endDisplay = True

        sleep(1)

        redLight.off()
        blueLight.off()

        ser.close()

