import typing
import pygetwindow as gw
import screeninfo
from time import sleep
from pyldplayer2.base.utils.wnd import activate_wnd


def get_screen_dimensions(monitor_index=0):
    """
    Returns the dimensions and position of a specific monitor.

    Args:
        monitor_index (int, optional): The index of the monitor to retrieve information from. Defaults to 0.

    Returns:
        tuple: A tuple containing the width, height, x-coordinate, and y-coordinate of the monitor.

    Raises:
        ValueError: If the monitor_index is invalid.

    """
    monitors = screeninfo.get_monitors()
    if monitor_index < 0 or monitor_index >= len(monitors):
        raise ValueError("Invalid monitor index")
    monitor = monitors[monitor_index]
    # Return both dimensions and the position of the monitor
    return (monitor.width, monitor.height, monitor.x, monitor.y)


def grid_orientation(
    wnds: typing.List[gw.Win32Window],
    row: int,
    col: int,
    maxwidth: float | None = None,
    maxheight: float | None = None,
    minwidth: float | None = None,
    minheight: float | None = None,
    monitor: int = 0,
    sleepTime: float = 0.2,
):
    """
    Arrange the given windows in a grid layout with the specified number of rows and columns.

    Args:
        wnds (List[gw.Window]): The list of windows to arrange.
        row (int): The number of rows in the grid layout.
        col (int): The number of columns in the grid layout.
        maxwidth (float, optional): The maximum width of each window. Defaults to None.
        maxheight (float, optional): The maximum height of each window. Defaults to None.
        minwidth (float, optional): The minimum width of each window. Defaults to None.
        minheight (float, optional): The minimum height of each window. Defaults to None.
        monitor (int, optional): The index of the monitor to use for the grid layout. Defaults to 0.
        sleepTime (float, optional): The time to sleep between each window arrangement. Defaults to 0.2.

    Returns:
        None

    Raises:
        None
    """

    screen_width, screen_height, monitor_x, monitor_y = get_screen_dimensions(
        monitor_index=monitor
    )
    num_windows = len(wnds)
    if num_windows == 0 or row == 0 or col == 0:
        return  # Early return if invalid input

    window_width = screen_width // col
    window_height = screen_height // row

    # Apply max and min dimensions
    if maxwidth is not None:
        window_width = min(window_width, maxwidth)
    if maxheight is not None:
        window_height = min(window_height, maxheight)
    if minwidth is not None:
        window_width = max(window_width, minwidth)
    if minheight is not None:
        window_height = max(window_height, minheight)

    for index, window_instance in enumerate(wnds):
        window_instance: gw.Win32Window
        new_x = (index % col) * window_width + monitor_x
        new_y = (index // col) * window_height + monitor_y

        activate_wnd(window_instance)
        window_instance.resizeTo(window_width, window_height)
        window_instance.moveTo(new_x, new_y)

        if index == row * col - 1:
            break

        sleep(sleepTime)
