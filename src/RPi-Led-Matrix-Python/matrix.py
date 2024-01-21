from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from datetime import datetime
import thermometer
import utilities

# set matrix options
options = RGBMatrixOptions()
# options.chain_length = 1
options.cols = 64
options.rows = 64
# options.parallel = 1
options.brightness = 15
# options.disable_hardware_pulsing = False
# options.drop_privileges = 1
options.gpio_slowdown = 4
options.hardware_mapping = "adafruit-hat-pwm"
# options.inverse_colors = False
# options.led_rgb_sequence = "RGB"
# options.multiplexing = 0
# options.pixel_mapper_config = ''
options.pwm_bits = 11
# options.pwm_dither_bits = 0
options.pwm_lsb_nanoseconds = 220
# options.row_address_type = 0
# options.scan_mode = 0
options.show_refresh_rate = False
options.limit_refresh_rate_hz = 120
matrix = RGBMatrix(options=options)

fonts = [
    "fonts/tom-thumb.bdf",
    "fonts/4x6.bdf",
    "fonts/5x7.bdf",
    "fonts/5x8.bdf",
    "fonts/6x9.bdf",
    "fonts/6x10.bdf",
    "fonts/6x12.bdf",
    "fonts/6x13.bdf",
    "fonts/6x13B.bdf",
    "fonts/6x13O.bdf",
    "fonts/8x13.bdf",
    "fonts/8x13B.bdf",
    "fonts/7x13.bdf",
    "fonts/7x14B.bdf",
]

def time_collector():
    current_time = datetime.now().strftime("%X")
    return current_time

def date_collector():
    current_date = datetime.today().strftime("%d/%m/%Y")
    return current_date

def matrix_display():
    temperature_font = graphics.Font()
    temperature_font.LoadFont(fonts[6])
    temperature_colour = graphics.Color(20, 220, 50)
    
    time_font = graphics.Font()
    time_font.LoadFont(fonts[13])
    time_colour = graphics.Color(77, 154, 77)

    calendar_font = graphics.Font()
    calendar_font.LoadFont(fonts[5])
    calendar_colour = graphics.Color(200, 50, 50)
    
    pomodoro_font = graphics.Font()
    pomodoro_font.LoadFont(fonts[13])
    pomodoro_colour = graphics.Color(200, 175, 0)
                                 
    break_font = graphics.Font()
    break_font.LoadFont(fonts[13])
    break_colour = graphics.Color(0, 0, 220)
 
    thermometer.init()
    utilities.init()
 
    canvas = matrix.CreateFrameCanvas()
    while True:
        canvas.Clear()
        time_on_matrix(canvas,time_font, time_colour)
        date_on_matrix(canvas,calendar_font, calendar_colour)
        temperature_on_matrix(canvas,temperature_font, temperature_colour)
        pomodoro_on_matrix(canvas,pomodoro_font,pomodoro_colour)
        break_time_on_matrix(canvas,break_font,break_colour)
        canvas = matrix.SwapOnVSync(canvas)

def temperature_on_matrix(canvas,temperature_font, temperature_colour):
    graphics.DrawText(canvas, temperature_font, 11, 57, temperature_colour, thermometer.roomTemp)

def date_on_matrix(canvas,calendar_font, calendar_colour):
    curernt_date = date_collector()
    graphics.DrawText(canvas, calendar_font, 3, 45, calendar_colour, curernt_date)

def time_on_matrix (canvas,time_font, time_colour):
    current_time = time_collector()
    graphics.DrawText(canvas, time_font, 4, 35, time_colour, current_time)
    
def pomodoro_on_matrix(canvas,font,colour):
    if utilities.pomodoro_state is True:
        graphics.DrawText(canvas, font, 15, 20, colour, convert_seconds(utilities.pomodoro_time))

def break_time_on_matrix(canvas,font,colour):
    if utilities.pomodoro_state is None:
        graphics.DrawText(canvas, font, 15, 20, colour, convert_seconds(utilities.pomodoro_time))            
        
def convert_seconds(total_seconds):
  """Converts seconds to minutes and seconds in a formatted string."""
  minutes = int(total_seconds // 60)
  seconds = int(total_seconds % 60)
  return f"{minutes:02d}:{seconds:02d}"  # Formatted output with leading zeros
