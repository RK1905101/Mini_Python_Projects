#!/usr/bin/python3
# -----------------------------------------------------------------
# simple pomodoro app using tkinter;
# this is one of my 50 python project challenge;
#
#
# Author:N84.
#
# Create Date:Sat Oct 22 20:24:56 2022.
# ///
# ///
# ///
# -----------------------------------------------------------------
from defaults import Defaults
from defaults import OS_NAME
import time
import tkinter as tk
from custom_thread import CustomThread
from sys import exit


# TODO: add reset button that appears only when we stop the timer;


Defaults.clear()


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(Defaults.TITLE)

        # set the size of the window;
        self.geometry(f"{Defaults.WIN_WIDTH}x{Defaults.WIN_HEIGHT}")

        # set the background color;
        self.configure(bg=Defaults.BACKGROUND_COLOR)

        # make the window un-resizable;
        self.resizable(0, 0)

        # set the minimum size for the window;
        self.minsize(width=Defaults.WIN_WIDTH, height=Defaults.WIN_HEIGHT)

        # self.protocol("WM_DELETE_WINDOW", lambda: print("resize"))

        # load all the images;
        self.images = self.__load_images()

        # setup the timer var for the label;
        # this variable will update our time on the screen;

        self.timer_value = tk.StringVar()
        # set default value for this var;
        self.timer_value.set("00:03")

        # create the window widgets;
        self.timer_label = tk.Label(
            master=self,
            textvariable=self.timer_value,
            **Defaults.TIMER_LABEL_PROPERTIES
        )

        if OS_NAME == "posix":
            # bind the mouse wheel with event;
            # this bind in case of linux;
            self.timer_label.bind("<Button-4>", self.__mouse_wheel_event)
            self.timer_label.bind("<Button-5>", self.__mouse_wheel_event)

        elif OS_NAME == "windows":
            self.timer_label.bind("<MouseWheel>", self.__mouse_wheel_event)

        self.btn = tk.Button(
            master=self,
            command=self.__btn_event,
            image=self.images["play_white"],
            text="click",
            ** Defaults.BTN_PROPERTIES
        )

        # now place all the widgets after creating them;
        self.place()

        # setup the timer status,
        # that we will use it for stop and staring the timer;
        # False for stop the timer and True for start the timer;
        self.__timer_status = False

        # set the tick-thread;

        self.__tick_thread = CustomThread(
            func=self.__timer_tick, name="tick_thread"
        )

        self.__blinking_thread = CustomThread(
            func=self.__label_blinking, name="label_blinking"
        )

        self.start_app()

    def place(self):
        """
            place all the widgets on the window;
        """

        # place the label;

        timer_label_x_coords, timer_label_y_coords = self.center_widget(
            widget=self.timer_label)

        self.timer_label.place(x=timer_label_x_coords, y=timer_label_y_coords)

        # place the button;
        btn_x_coords, btn_y_coords = self.center_widget(
            widget=self.btn, y_factor=1.3)
        self.btn.place(x=btn_x_coords, y=btn_y_coords)

    def center_widget(self, widget, y_factor=2, x_factor=2):
        """
            center any widget;


            return tuple(x:int, y:int);
        """
        window_width, window_height = self.winfo_width(), self.winfo_height()

        # guard-condition;
        if window_height + window_width < 10:
            window_width, window_height = Defaults.WIN_WIDTH, Defaults.WIN_HEIGHT

        widget_x_coords = (window_width -
                           widget.winfo_reqwidth()) // x_factor
        widget_y_coords = (window_height -
                           widget.winfo_reqheight()) // y_factor

        return widget_x_coords, widget_y_coords

    def start_app(self, **options):
        """
            start the app;
        """

        self.mainloop()

    def __load_images(self):
        """
            load all needed images;

            return dict;
        """
        # import our pictures.

        play_white_pic = tk.PhotoImage(
            file="./assests/pictures/play_white.png", name="play_white")

        pause_white_pic = tk.PhotoImage(
            file="./assests/pictures/pause_white.png", name="pause_white")

        return {
            "play_white": play_white_pic,
            "pause_white": pause_white_pic
        }

    def timer_value_to_seconds(self):
        """
            convert the timer value in the label,
            into seconds as an integer;

            return seconds:int
        """

        # get the time from the timer label, the minutes and seconds;
        timer_label_value_minutes, timer_label_value_seconds = self.timer_value.get().split(":")

        # and turn it to seconds;
        timer_value_in_seconds = int(
            timer_label_value_minutes) * 60 + int(timer_label_value_seconds)

        return timer_value_in_seconds

    def seconds_to_timer_value(self, timer_value_in_seconds: int):
        """
            convert the total seconds value to the string,
            timer format;

            return timer_value:str
        """

        time_in_minutes, time_in_seconds = divmod(timer_value_in_seconds, 60)
        timer_new_value = f"{str(time_in_minutes).zfill(2)}:{str(time_in_seconds).zfill(2)}"

        return timer_new_value

    def __timer_tick(self):
        """
            start the timer or stop it;
        """

        # and turn it to seconds;
        timer_value_in_seconds = self.timer_value_to_seconds()

        while timer_value_in_seconds > -1 and self.__timer_status:

            timer_new_value = self.seconds_to_timer_value(
                timer_value_in_seconds)

            timer_value_in_seconds -= 1

            # now update the timer value;
            self.timer_value.set(timer_new_value)
            time.sleep(1)

        if self.__timer_status:
            # set the timer after its done;
            self.timer_value.set("15:00")

            # and then call the button event to,
            # change the button and stop the thread;
            self.__btn_event()

        return None

    def __btn_event(self):
        """
            start/pause button event;

            return None
        """

        # self.place() # DEBUG;

        if self.btn.cget("image") == "play_white":

            self.btn.configure(image=self.images["pause_white"])
            self.__timer_status = True

            try:
                # self.__tick_thread.start()
                self.__tick_thread.run()

            except RuntimeError:
                # if we click on the button multiple times;
                print("Timer Tick Threading!")
                return None

        elif self.btn.cget("image") == "pause_white":

            self.btn.configure(image=self.images["play_white"])
            self.__timer_status = False

            try:
                self.__blinking_thread.run()

            except RuntimeError:
                print("blinking Threading!")
                return None

        return None

    def __label_blinking(self):
        """
            simple event that will cause to change the color of the,
            label to blue then to the white if we stop the timer,
            and keep blinking until we start the timer again;

            return None;
        """

        while not self.__timer_status:

            self.timer_label.configure(fg=Defaults.LABEL_BLINKING_FG)
            self.update()
            time.sleep(0.5)  # sleep for half millisecond;

            self.timer_label.configure(fg=Defaults.LABEL_FG_BASE)
            self.update()
            time.sleep(0.5)  # sleep for half millisecond;

        return None

    def __mouse_wheel_event(self, e):
        """
            when the mouse wheel is moving then,
            either increase the timer label or,
            decrease it;

            return None;
        """

        if self.__timer_status:
            # if the timer is active;
            # aka the timer start ticking
            return

        timer_in_seconds = self.timer_value_to_seconds()

        # the value that we increase or decrease,
        # either in our minutes or seconds;
        # in case of minutes we add or remove 60 seconds,
        # and that is obvious, and in case of seconds,
        # we add or remove 1 second;
        value = 60 if e.x < 47 else 1

        MAX_VALUE = 99 * 60  # 99 minutes;
        MIN_VALUE = 0

        if e.num == 4:
            # in case of increasing the event.num is 4;

            if timer_in_seconds > MAX_VALUE:
                self.timer_value.set("99:59")

                return None

            timer_in_seconds += value

        if e.num == 5:

            # in case of decreasing the event.num is 5;

            # guard condition;
            if timer_in_seconds <= MIN_VALUE:
                # if its zero;
                self.timer_value.set("00:00")
                return None

            timer_in_seconds -= value

        timer_new_value = self.seconds_to_timer_value(timer_in_seconds)

        self.timer_value.set(timer_new_value)

        return None


def main():
    app = App()


if __name__ == "__main__":
    main()
