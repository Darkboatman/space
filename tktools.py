import tkinter

def fix_system_zoom():
    import sys
    if sys.platform == 'win32':
        try:
            import ctypes
            PROCESS_SYSTEM_DPI_AWARE = 1  # Int required.
            ctypes.OleDLL('shcore').SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
        except (ImportError, AttributeError, OSError):
            pass


def init_tk():
    fix_system_zoom()
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root,bg='black')
    canvas.pack(fill='both', expand=True)
    root.state('zoomed')
    return root,canvas
