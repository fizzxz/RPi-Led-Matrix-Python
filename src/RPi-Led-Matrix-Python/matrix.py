from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import datetime
import thermometer
import utilities
from metoffice.metoffice import curr_weather_forecast
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
    current_time = datetime.datetime.now().strftime("%X")
    return current_time

def date_collector():
    current_date = datetime.datetime.today().strftime("%d/%m/%Y")
    return current_date

def matrix_display():
    temperature_font = graphics.Font()
    temperature_font.LoadFont(fonts[6])
    # temperature_colour = graphics.Color(20, 220, 50)
    temperature_colour = graphics.Color(215, 54, 101)
    
    time_font = graphics.Font()
    time_font.LoadFont(fonts[13])
    # time_colour = graphics.Color(77, 154, 77)

    calendar_font = graphics.Font()
    calendar_font.LoadFont(fonts[5])
    
    pomodoro_font = graphics.Font()
    pomodoro_font.LoadFont(fonts[13])
    pomodoro_colour = graphics.Color(200, 175, 0)
                                 
    break_font = graphics.Font()
    break_font.LoadFont(fonts[13])
    break_colour = graphics.Color(0, 0, 220)
 
    weather_font = graphics.Font()
    weather_font.LoadFont(fonts[5])
    weather_cond_font = graphics.Font()
    weather_cond_font.LoadFont(fonts[3])
    weather_text,weather_cond= curr_weather_forecast()
    #  print(f"Temperature: {current_weather['T']}°C")
    # print(f"Wind: {current_weather['D']} {current_weather['S']} mph")
    # print(f"Conditions: {weather_cond}")
    print(weather_text)
    print(weather_cond)
    thermometer.init()
    utilities.init()
    # set default value to clock
    utilities.scene_type = "clock"
 
    canvas = matrix.CreateFrameCanvas()
    while True:
        canvas.Clear()
        time_colour,calendar_colour=change_colour()
        if utilities.scene_type == "clock":
            time_on_matrix(canvas,time_font, time_colour)
            date_on_matrix(canvas,calendar_font, calendar_colour)
            temperature_on_matrix(canvas,temperature_font, temperature_colour)
            pomodoro_on_matrix(canvas,pomodoro_font,pomodoro_colour)
            break_time_on_matrix(canvas,break_font,break_colour)
        elif utilities.scene_type == "weather":   
            current_time = time_collector()
            graphics.DrawText(canvas, time_font, 4, 15, time_colour, current_time)
            weather_disp_text(canvas,weather_font,temperature_colour,weather_text,weather_cond,weather_cond_font)

        canvas = matrix.SwapOnVSync(canvas)

def weather_disp_text(canvas, font, font_colour,weather_text,weather_cond,weather_cond_font):
    graphics.DrawText(canvas,font,1, 25, font_colour, str(f"T:{weather_text['T']}°C"))
    graphics.DrawText(canvas,font,1, 35, font_colour, str(f"W: {weather_text['D']} {weather_text['S']} mph"))
    split_weather_cond=weather_cond.split()
    if len(split_weather_cond)>=1:
        graphics.DrawText(canvas,weather_cond_font,1, 44, font_colour, str(f"{split_weather_cond[0]}"))
    if len(split_weather_cond) >= 2:
        graphics.DrawText(canvas,weather_cond_font,35, 44, font_colour, str(f"{split_weather_cond[1]}"))
    if len(split_weather_cond) >= 3:
        graphics.DrawText(canvas,weather_cond_font,1, 52, font_colour, str(f"{split_weather_cond[2]}"))
    if len(split_weather_cond) >= 4:
        graphics.DrawText(canvas,weather_cond_font,1, 62, font_colour, str(f"{split_weather_cond[3]}"))
        
        


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

def change_colour():
   time_colour,calendar_colour= execute_function_based_on_time()
   return time_colour,calendar_colour
    

def convert_seconds(total_seconds):
  """Converts seconds to minutes and seconds in a formatted string."""
  minutes = int(total_seconds // 60)
  seconds = int(total_seconds % 60)
  return f"{minutes:02d}:{seconds:02d}"  # Formatted output with leading zeros


def change_colour_for_0600_to_1200():
    time_colour = graphics.Color(140, 29, 42)
    calendar_colour = graphics.Color(140,29, 45)
    return time_colour,calendar_colour

def change_colour_for_1200_to_1800():
    time_colour = graphics.Color(215, 54, 101)
    calendar_colour = graphics.Color(200, 50, 50) 
    return time_colour,calendar_colour

def change_colour_for_1800_to_0000():
    time_colour = graphics.Color(199, 44, 137)
    calendar_colour = graphics.Color(199, 50, 50)
    return time_colour,calendar_colour

def change_colour_for_0000_to_0600():
    time_colour = graphics.Color(54, 54, 54)
    calendar_colour = graphics.Color(54, 54, 54)
    return time_colour,calendar_colour

def execute_function_based_on_time():
    current_time = datetime.datetime.now().time()
    time_colour = graphics.Color(77, 154, 77)
    calendar_colour = graphics.Color(77, 154, 77)

    time_ranges = [
        ((5, 0), change_colour_for_0600_to_1200),
        ((11, 0), change_colour_for_1200_to_1800),
        ((17, 0), change_colour_for_1800_to_0000),
        ((1, 0), change_colour_for_0000_to_0600)
    ]
    for start_time, func in time_ranges:
        start_time_obj = datetime.time(*start_time)
        end_time_obj = (datetime.datetime.combine(datetime.datetime.today(), start_time_obj) + datetime.timedelta(hours=6)).time()
        if start_time_obj <= current_time <= end_time_obj:
            time_colour,calendar_colour=func()
            return time_colour,calendar_colour
    else:
        # print("No matching time range found.")
        return time_colour,calendar_colour
