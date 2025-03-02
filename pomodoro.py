import time
import argparse
from AppKit import (
    NSApplication,
    NSWindow,
    NSView,
    NSTextField,
    NSButton,
    NSApp,
    NSWorkspace,
    NSMakeRect,
    NSAttributedString,
    NSFont,
    NSColor,
    NSCenterTextAlignment,
    NSBorderlessWindowMask,
    NSTimer,
    NSDate,
    NSDefaultRunLoopMode,
    NSWindowStyleMaskBorderless,
    NSBackingStoreBuffered,
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    NSBezelBorder,
    NSWindowStyleMaskTitled,
    NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable,
    NSWindowStyleMaskFullSizeContentView,
)
from Quartz import kCGMaximumWindowLevel

class DraggableWindow(NSWindow):
    def mouseDown_(self, event):
        self.initialLocation = event.locationInWindow()

    def mouseDragged_(self, event):
        screenOrigin = self.screen().frame().origin
        windowOrigin = self.frame().origin
        newLocation = event.locationInWindow()
        newX = windowOrigin.x + newLocation.x - self.initialLocation.x
        newY = windowOrigin.y - (newLocation.y - self.initialLocation.y)
        self.setFrameOrigin_((newX, newY))

class PomodoroApp:
    def __init__(self, num_sessions, work_time, short_break, long_break):
        self.num_sessions = num_sessions
        self.work_time = work_time
        self.short_break = short_break
        self.long_break = long_break
        self.seconds = 0
        self.display_text = ""
        self.timer = None
        self.is_running = False
        self.session_count = 0
        self.setup_ui()
        self.speak = ""

    def setup_ui(self):
        self.app = NSApplication.sharedApplication()
        self.window = DraggableWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 300, 150),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskFullSizeContentView,
            NSBackingStoreBuffered,
            False,
        )
        self.window.setLevel_(kCGMaximumWindowLevel)
        self.window.setOpaque_(True)
        self.window.setBackgroundColor_(NSColor.darkGrayColor())
        self.window.setHasShadow_(True)
        self.window.setTitle_("Pomodoro Timer")
        self.window.center()
        self.window.makeKeyAndOrderFront_(None)

        self.view = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 300, 150))
        self.window.setContentView_(self.view)

        self.timer_label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 30, 280, 40))
        self.timer_label.setStringValue_("Time: 00:00")
        self.timer_label.setEditable_(False)
        self.timer_label.setBezeled_(False)
        self.timer_label.setDrawsBackground_(True)
        self.timer_label.setBackgroundColor_(NSColor.blackColor())
        self.timer_label.setAlignment_(NSCenterTextAlignment)
        font = NSFont.boldSystemFontOfSize_(30)
        text_color = NSColor.lightGrayColor()
        attributes = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: text_color,
        }
        attributed_string = NSAttributedString.alloc().initWithString_attributes_("Time: 00:00", attributes)
        self.timer_label.setAttributedStringValue_(attributed_string)
        self.view.addSubview_(self.timer_label)

        self.start_button = NSButton.alloc().initWithFrame_(NSMakeRect(100, 80, 100, 30))
        self.start_button.setTitle_("Start")
        self.start_button.setBezelStyle_(NSBezelBorder)
        self.start_button.setTarget_(self)
        self.start_button.setAction_("start_stop_timer:")
        self.view.addSubview_(self.start_button)
        self.start_button.setWantsLayer_(True)
        self.start_button.layer().setBackgroundColor_(NSColor.grayColor().CGColor())
        self.start_button.layer().setBorderWidth_(1)
        self.start_button.layer().setCornerRadius_(5)

        self.speak_label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 5, 280, 20))
        self.speak_label.setStringValue_("")
        self.speak_label.setEditable_(False)
        self.speak_label.setBezeled_(False)
        self.speak_label.setDrawsBackground_(False)
        self.speak_label.setAlignment_(NSCenterTextAlignment)
        font = NSFont.systemFontOfSize_(10)
        text_color = NSColor.whiteColor()
        attributes = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: text_color,
        }
        attributed_string = NSAttributedString.alloc().initWithString_attributes_("", attributes)
        self.speak_label.setAttributedStringValue_(attributed_string)
        self.view.addSubview_(self.speak_label)

    def start_stop_timer_(self, sender):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.is_running = True
        self.start_button.setTitle_("Stop")

        if self.session_count % (self.num_sessions * 2) == 0:
            self.work(self.work_time)
        elif self.session_count % 2 == 1 :
            self.take_break(self.short_break)
        elif self.session_count % (self.num_sessions * 2) == (self.num_sessions * 2) - 1:
            self.take_break(self.long_break)
        else :
            self.take_break(self.short_break)

    def stop_timer(self):
        self.is_running = False
        if self.timer:
            self.timer.invalidate()
            self.timer = None
        self.start_button.setTitle_("Start")

    def work(self, minutes):
        self.display_text = "Work Time"
        self.count_down(minutes)
        self.session_count += 1
        self.speak = "YOU HAVE TO BE WILLING TO GO TO WAR WITH YOURSELF"

    def take_break(self, minutes):
        self.display_text = "Break Time"
        self.count_down(minutes)
        self.session_count += 1
        self.speak = "TAKE A WELL DESERVED BREAK!"

    def count_down(self, minutes):
        self.seconds = minutes * 60
        self.update_timer()
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, "timer_tick:", None, True
        )

    def timer_tick_(self, timer):
        self.seconds -= 1
        self.update_timer()
        if self.seconds <= 0:
            self.timer.invalidate()
            self.timer = None
            self.start_stop_timer_(None)

    def update_timer(self): 
        mins, secs = divmod(self.seconds, 60) 
        timer_display = f"{mins:02d}:{secs:02d}" 
        message = f"{self.display_text}: {timer_display}" 
        font = NSFont.boldSystemFontOfSize_(30) 
        text_color = NSColor.lightGrayColor() 
        self.speak_label.setStringValue_(self.speak)
        attributes = { 
            NSFontAttributeName: font, 
            NSForegroundColorAttributeName: text_color, 
        } 
        attributed_string = NSAttributedString.alloc().initWithString_attributes_(message, attributes) 
        self.timer_label.setAttributedStringValue_(attributed_string)

def cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_sessions', type=int, default=4, help="Number of smaller sessions before a longer break")
    parser.add_argument('--work', type=int, default=30, help="Work session duration in minutes")
    parser.add_argument('--short_break', type=int, default=5, help="Duration of a short break")
    parser.add_argument('--long_break', type=int, default=30, help="Duration of a long break")
    return parser.parse_args()

def main():
    args = cmd_args()
    print(f"Starting a {args.work}-minute Pomodoro session...")
    app = PomodoroApp(args.num_sessions, args.work, args.short_break, args.long_break)
    NSApp.run()

if __name__ == "__main__":
    main()