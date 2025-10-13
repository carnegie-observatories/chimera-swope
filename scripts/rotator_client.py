from nicegui import run, ui
from nicegui.events import ValueChangeEventArguments
from chimera.core.proxy import Proxy


class RotatorClient:

    def show(self, event: ValueChangeEventArguments):
        name = type(event.sender).__name__
        ui.notify(f"{name}: {event.value}")
        pass

    def update_pa_offset(self, pa):
        print("Updating PA offset:", pa)
        self.offset_pa = pa

    def update_rotator_pa(self, angle):
        self.current_pa = f"{angle:.3f}º"

    def move_btn(self):
        ui.notify(f"Offsetting rotator by {self.offset_pa:.3f}º")
        self.rotator_proxy.move_by(self.offset_pa)
        self.offset_pa = 0.0
        self.update_pa_offset(self.offset_pa)

    def set_pa_offset(self, event: ValueChangeEventArguments):
        self.offset_pa = float(event.value)

    def get_display_proxy_pa(self, detect_stars=True):
        return self.display_proxy.get_pa(detect_stars=detect_stars)

    async def grab_stars_btn(self):
        ui.notify("Grabbing PA from DS9")
        await run.cpu_bound(self.get_display_proxy_pa, detect_stars=True)
        ui.notify("Finished grabbing PA from DS9")

    async def grab_pixels_btn(self):
        ui.notify("Grabbing PA from DS9 (2 points)")
        await run.cpu_bound(self.get_display_proxy_pa, detect_stars=False)
        ui.notify("Finished grabbing PA from DS9 (2 points)")

    def __init__(self):
        self.display_proxy = Proxy("127.0.0.1:6379/Ds9AutoDisplay/display")
        self.display_proxy.update_pa += self.update_pa_offset
        self.rotator_proxy = Proxy("127.0.0.1:6379/FakeRotator/rotator")
        self.rotator_proxy.slew_complete += self.update_rotator_pa

        self.update_rotator_pa(self.rotator_proxy.get_position())
        self.offset_pa = 0.0
        self.draw()

    def draw(self):

        with ui.row():
            ui.input("Current PA:").bind_value(self, "current_pa").props("readonly")
            ui.input("Offset PA:", on_change=self.set_pa_offset).bind_value(
                self, "offset_pa"
            )
            ui.button("Grab Stars", on_click=self.grab_stars_btn)
            ui.button("Grab Pixels", on_click=self.grab_pixels_btn)
        with ui.row():
            ui.button("Move", on_click=self.move_btn)


r = RotatorClient()

ui.run(native=True, title="Rotator Client", dark=True, reload=True)
