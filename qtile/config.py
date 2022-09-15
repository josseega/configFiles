# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "qutebrowser" # My terminal of choice

keys = [

    #### Shortcuts ####
    ###################
    ### Switch focus of monitors
    Key([mod], "backslash",
     lazy.next_screen(),
     desc='Move focus to next monitor'
     ),
    Key([mod], "comma",
     lazy.prev_screen(),
     desc='Move focus to prev monitor'
     ),

    Key([mod], "Return",
        lazy.spawn("alacritty"),
        desc="Launch terminal"),

    Key([mod, "shift"], "Return",
        lazy.spawn("rofi -show drun"),
        desc="Open Menu"),

    Key([mod], "i",
        lazy.spawn(myBrowser),
        desc="Open Qutebrowser"),

    Key([mod, "control"], "i",
        lazy.spawn("firefox"),
        desc="Open Firefox"),

    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toogle a fullscreen"),

    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
        ),
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows

        ### Window controls
   Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
   Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
   Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
   Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
   Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
   # Move windows between left/right columns or move up/down in current stack.
   # Moving out of range in Columns layout will create new column.
   Key([mod, "shift"], "h", lazy.layout.move_left(), desc="Move window to the left"),
   Key([mod, "shift"], "l", lazy.layout.move_right(), desc="Move window to the right"),
   Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
   Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
   # Grow windows. If current window is on the edge of screen and direction
   # will be to screen edge - window would shrink.
   
    Key([mod, "control"], "j",
       lazy.layout.shrink(),
       desc="Grow window to the left"),

   Key([mod, "control"], "k",
       lazy.layout.grow(),
       desc="Grow window to the right"),

   Key([mod], "n",
       lazy.layout.normalize(),
       desc="Reset all window sizes"),

    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
        ),

   # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "p", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group("DEV", layout='monadtall'),
          Group("TeX", layout='monadtall'),
          Group("DOC", layout='monadtall'),
          Group("WEB", layout='monadtall'),
          Group("CHAT", layout='monadtall'),
          Group("MAIL", layout='monadtall'),
          Group("SYS", layout='monadtall'),
          Group("MUS", layout='monadtall')]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 6,
                "margin": 8,
                "border_focus": "#602ac3",
                "border_normal": "#1D2330"
                }

layouts = [
    layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    #layout.Stack(num_stacks=2),
    #layout.RatioTile(**layout_theme),
#    layout.TreeTab(
#         font = "Ubuntu",
#         fontsize = 10,
#         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
#         section_fontsize = 10,
#         border_width = 2,
#         bg_color = "1c1f24",
#         active_bg = "c678dd",
#         active_fg = "000000",
#         inactive_bg = "a9a1e1",
#         inactive_fg = "1c1f24",
#         padding_left = 0,
#         padding_x = 0,
#         padding_y = 5,
#         section_top = 10,
#         section_bottom = 20,
#         level_shift = 8,
#         vspace = 3,
#         panel_width = 200
#         ),
#    layout.Floating(**layout_theme)
]

colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#576b80", "#576b80"],
          ["#80576b", "#80576b"]]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 10,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Image(
                       filename = "~/.config/qtile/icons/python-white.png",
                       scale = "False",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 9,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2],
                       background = colors[0],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[0],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),
              widget.Prompt(
                       foreground = colors[2],
                       background = colors[0],
                       padding = 5
                      ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
                widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = colors[9],
                       padding = -12,
                       fontsize = 60
                       ),
             widget.Net(
                       interface = "wlan0",
                       format = 'Net: {down} ↓↑ {up}',
                       foreground = colors[2],
                       background = colors[9],
                       padding = 5
                       ),
                widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[9],
                       foreground = colors[10],
                       padding = -12,
                       fontsize = 60
                       ),
              widget.ThermalSensor(
                       foreground = colors[2],
                       background = colors[10],
                       threshold = 90,
                       fmt = 'Temp: {}',
                       padding = 5
                       ),
              widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch",
                       display_format = "Updates: {updates} ",
                       foreground = colors[1],
                       colour_have_updates = colors[1],
                       colour_no_updates = colors[1],
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + '-e sudo pacman -Syu')},
                       padding = 5,
                       background = colors[5]
                       ),
                widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[10],
                       foreground = colors[9],
                       padding = -12,
                       fontsize = 60
                       ),
              widget.Memory(
                       foreground = colors[2],
                       background = colors[9],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       fmt = 'Mem: {}',
                       padding = 5
                       ),
                widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[9],
                       foreground = colors[10],
                       padding = -12,
                       fontsize = 60
                       ),
              widget.Volume(
                       foreground = colors[2],
                       background = colors[10],
                       fmt = 'Vol: {}',
                       padding = 5
                       ),
                widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[10],
                       foreground = colors[9],
                       padding = -12,
                       fontsize = 60
                       ),
              widget.KeyboardLayout(
                       configured_keyboards = ['us','latam'],
                       foreground = colors[2],
                       background = colors[9],
                       padding = 5
                       ),
                widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[9],
                       foreground = colors[10],
                       padding = -12,
                       fontsize = 60
                       ),
              widget.Clock(
                       foreground = colors[2],
                       background = colors[10],
                       format = "%A, %B %d - %H:%M "
                       ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[10:24]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

    #return [Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.9, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"
