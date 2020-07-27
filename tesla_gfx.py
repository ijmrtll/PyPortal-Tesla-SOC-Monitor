# object to manage the graphics GFX

import time
import board
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload


cwd = ("/"+__file__).rsplit('/', 1)[0]

small_font = cwd+"/fonts/Arial-12.bdf"
medium_font = cwd+"/fonts/Arial-16.bdf"
large_font = cwd+"/fonts/Arial-Bold-24.bdf"

class Tesla_gfx(displayio.Group):
    def __init__(self, root_group, *, debug=False):
        super().__init__(max_size=5)
        self._debug = debug
        self._SOC = 'NA' #Last known batery SOC
        
        root_group.append(self)
        self._background_group = displayio.Group(max_size=1)
        self._icon_group = displayio.Group(max_size=1)
        self.append(self._background_group)
        self.append(self._icon_group)
        self._text_group = displayio.Group(max_size=5)
        self.append(self._text_group)
 
        self._icon_sprite = None
        self._icon_file = None
        self._bg_sprite = None
        self._bg_file = None
        self.set_icon(cwd+"/tesla_logo.bmp")
 
        self.small_font = bitmap_font.load_font(small_font)
        self.medium_font = bitmap_font.load_font(medium_font)
        self.large_font = bitmap_font.load_font(large_font)
        glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
        self.small_font.load_glyphs(glyphs)
        self.medium_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(glyphs)
        
        #Loading screen text
        self.loading_text = Label(self.medium_font, max_glyphs=11)
        self.loading_text.color = 0xFFFFFF
        self._text_group.append(self.loading_text)
        
        #SOC screen text
        self.bat_text = Label(self.large_font, max_glyphs=8)
        self.bat_text.color = 0xFFFFFF
        self.bat_text.x = 123
        self.bat_text.y = 65
        self._text_group.append(self.bat_text)
        
        #SLP screen text
        self.slp_text = Label(self.large_font, max_glyphs=8)
        self.slp_text.color = 0xFFFFFF
        self.slp_text.x = 123
        self.slp_text.y = 65
        self._text_group.append(self.slp_text)
        
        self.bat_pos = (120, 85) # this is the position of the battery icon
        
        #Charging text/icon pos
        self.charging_pos = (200, 20) # this is the position of the charging icon

    def append_background(self):
        if self._bg_file:
            self._bg_file.close()
        self._bg_file = open(cwd + "/Tesla_Car.bmp", "rb")
        bg = displayio.OnDiskBitmap(self._bg_file)
        try:
            self._bg_sprite = displayio.TileGrid(bg,
            pixel_shader=displayio.ColorConverter())
        except TypeError:
            self._bg_sprite = displayio.TileGrid(bg,
            pixel_shader=displayio.ColorConverter(),
            position=(0,0))
        self._background_group.append(self._bg_sprite)
        board.DISPLAY.refresh_soon()
        board.DISPLAY.wait_for_frame()
        
    def display_loading(self, text="loading...."):
        self.loading_text.text = text
        self.loading_text.x = 123
        self.loading_text.y = 65
        self.set_icon(cwd + "/icons/"+"loading.bmp", self.bat_pos)
    
    def display_bat(self, bat, chrg):
        
        if isinstance(bat, str):
            if bat == "NA":
                self.slp_text.text = " SLP"
                self.slp_text.x = 123
                self.slp_text.y = 35
                self.bat_text.text = " " + self._SOC + " %"
                self.set_icon(cwd+"/icons/"+"NA.bmp", self.bat_pos)

        else:
            self._SOC = str(bat)
            self.bat_text.text = " " + str(bat) + " %"
            self.bat_text.x = 123
            self.bat_text.y = 65
            if(chrg != "Disconnected"):
                if bat <= 5:
                    self.set_icon(cwd+"/icons/"+"5_chg.bmp", self.bat_pos)
                if bat > 5 and bat <= 25:
                    self.set_icon(cwd+"/icons/"+"25_chg.bmp", self.bat_pos)
                if bat > 25 and bat <= 45:
                    self.set_icon(cwd+"/icons/"+"45_chg.bmp", self.bat_pos)
                if bat > 45 and bat <= 65:
                    self.set_icon(cwd+"/icons/"+"65_chg.bmp", self.bat_pos)
                if bat > 65 and bat <= 85:
                    self.set_icon(cwd+"/icons/"+"85_chg.bmp", self.bat_pos)
                if bat > 85:
                    self.set_icon(cwd+"/icons/"+"100_chg.bmp", self.bat_pos)
            else:
                if bat <= 5:
                    self.set_icon(cwd+"/icons/"+"5.bmp", self.bat_pos)
                if bat > 5 and bat <= 25:
                    self.set_icon(cwd+"/icons/"+"25.bmp", self.bat_pos)
                if bat > 25 and bat <= 45:
                    self.set_icon(cwd+"/icons/"+"45.bmp", self.bat_pos)
                if bat > 45 and bat <= 65:
                    self.set_icon(cwd+"/icons/"+"65.bmp", self.bat_pos)
                if bat > 65 and bat <= 85:
                    self.set_icon(cwd+"/icons/"+"85.bmp", self.bat_pos)
                if bat > 85:
                    self.set_icon(cwd+"/icons/"+"100.bmp", self.bat_pos)

    def set_icon(self, filename, xy=(0,0)):

        if self._debug:
            print("Set icon to ", filename)
        if self._icon_group:
            self._icon_group.pop()
 
        if not filename:
            return  # we're done, no icon desired
        if self._icon_file:
            self._icon_file.close()
        self._icon_file = open(filename, "rb")
        icon = displayio.OnDiskBitmap(self._icon_file)
        try:
            self._icon_sprite = displayio.TileGrid(icon,
            pixel_shader=displayio.ColorConverter())
            print(self._icon_sprite.pixel_shader)
        except TypeError:
            self._icon_sprite = displayio.TileGrid(icon,
            pixel_shader=displayio.ColorConverter(),
            position=(0,0))
        self._icon_group.append(self._icon_sprite)
        self._icon_group.x = xy[0]
        self._icon_group.y = xy[1]
        board.DISPLAY.refresh_soon()
        board.DISPLAY.wait_for_frame()
        
    
    #adds the local time.
    def update_time(self):
        """Fetch the time.localtime(), parse it out and update the display text"""
        now = time.localtime()
        self.time_hour = now[3]
        self.time_minute = now[4]
        format_str = "%d:%02d"
        self.time_str = format_str % (self.time_hour, self.time_minute)
    
    def clear_text(self):
        self.loading_text.text = []
        self.bat_text.text = []
        self.slp_text.text = []
        board.DISPLAY.refresh_soon()
        board.DISPLAY.wait_for_frame()