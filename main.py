from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
saved_pattern = ""



# -------- FLASH PATTERN STORAGE --------
flash_patterns = []      # all saved patterns
current_pattern = []     # pattern being created




# ---------------- SPLASH SCREEN ----------------
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.full_text = "WELCOME TO\nGURUKIRAN'S\nAPP"
        self.current_text = ""
        self.index = 0

        layout = FloatLayout()

        bg = Image(source="bg.png", allow_stretch=True, keep_ratio=False)

        self.text_label = Label(
            text="",
            font_size=36,
            halign="center",
            valign="middle",
            text_size=(Window.width, Window.height),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        layout.add_widget(bg)
        layout.add_widget(self.text_label)
        self.add_widget(layout)

        Clock.schedule_interval(self.type_text, 0.05)

    def type_text(self, dt):
        if self.index < len(self.full_text):
            self.current_text += self.full_text[self.index]
            self.text_label.text = self.current_text
            self.index += 1
        else:
            Clock.unschedule(self.type_text)
            Clock.schedule_once(self.go_to_main, 1)

    def go_to_main(self, dt):
        self.manager.current = "main"


# ---------------- MAIN SCREEN ----------------
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        self.label = Label(
            text="MAIN SCREEN",
            font_size=26,
            pos_hint={"center_x": 0.5, "center_y": 0.05}
        )
        layout.add_widget(self.label)

        # ALL BUTTONS
        self.flash_btn = Button(text="Smart Flashlight",
                                size_hint=(0.6, 0.1),
                                pos_hint={"center_x": 0.5, "center_y": 0.90})

        self.call_btn = Button(text="Auto Call / Reminder",
                               size_hint=(0.6, 0.1),
                               pos_hint={"center_x": 0.5, "center_y": 0.75})

        self.qr_btn = Button(text="QR Scanner",
                             size_hint=(0.6, 0.1),
                             pos_hint={"center_x": 0.5, "center_y": 0.60})

        self.doc_btn = Button(text="Document Scanner",
                              size_hint=(0.6, 0.1),
                              pos_hint={"center_x": 0.5, "center_y": 0.45})

        self.auto_btn = Button(text="Simple Automation",
                               size_hint=(0.6, 0.1),
                               pos_hint={"center_x": 0.5, "center_y": 0.30})

        self.store_btn = Button(text="Storage",
                                size_hint=(0.6, 0.1),
                                pos_hint={"center_x": 0.5, "center_y": 0.15})

        # ADD BUTTONS
        for btn in [self.flash_btn, self.call_btn, self.qr_btn,
                    self.doc_btn, self.auto_btn, self.store_btn]:
            layout.add_widget(btn)
            btn.bind(on_press=self.button_pressed)

        self.add_widget(layout)

    def button_pressed(self, instance):
        self.label.text = instance.text + " Pressed"

        if instance == self.flash_btn:
            self.manager.current = "saved_patterns"


# ---------------- SAVED PATTERNS ----------------
class SavedPatternsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()

        self.title = Label(
            text="Saved Flash Patterns",
            font_size=24,
            pos_hint={"center_x": 0.5, "center_y": 0.9}
        )

        self.list_label = Label(
            text="No patterns saved",
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )

        new_btn = Button(
            text="Create New Pattern",
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.35}
        )
        new_btn.bind(on_press=self.open_settings)

        back_btn = Button(
            text="BACK",
            size_hint=(0.4, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        back_btn.bind(on_press=self.go_back)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.list_label)
        self.layout.add_widget(new_btn)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        if flash_patterns:
            text = ""
            for i, p in enumerate(flash_patterns):
                text += f"Pattern {i+1}: {p}\n"
            self.list_label.text = text
        else:
            self.list_label.text = "No patterns saved"

    def open_settings(self, instance):
        self.manager.current = "flash_settings"

    def go_back(self, instance):
        self.manager.current = "main"



# ---------------- FLASH SETTINGS ----------------


class FlashSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        self.on_input = TextInput(
            hint_text="Flash ON time (seconds)",
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            multiline=False,
            input_filter='int'
        )

        self.off_input = TextInput(
            hint_text="Flash OFF time (seconds)",
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.50},
            multiline=False,
            input_filter='int'
        )

        save_btn = Button(
            text="ADD STEP",
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.35}
        )
        save_btn.bind(on_press=self.save_step)

        done_btn = Button(
            text="DONE",
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.22}
        )
        done_btn.bind(on_press=self.finish_pattern)

        back_btn = Button(
            text="BACK",
            size_hint=(0.4, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(self.on_input)
        layout.add_widget(self.off_input)
        layout.add_widget(save_btn)
        layout.add_widget(done_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def save_step(self, instance):
        if self.on_input.text and self.off_input.text:
            current_pattern.append(
                (int(self.on_input.text), int(self.off_input.text))
            )
            self.on_input.text = ""
            self.off_input.text = ""

    def finish_pattern(self, instance):
        if current_pattern:
            flash_patterns.append(list(current_pattern))
            current_pattern.clear()
        self.manager.current = "saved_patterns"

    def go_back(self, instance):
        self.manager.current = "saved_patterns"



# ---------------- APP ----------------
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SavedPatternsScreen(name="saved_patterns"))
        sm.add_widget(FlashSettingsScreen(name="flash_settings"))
        sm.current = "splash"
        return sm


MyApp().run()
