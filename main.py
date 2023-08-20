import multiprocessing as mp
import platform
import AppKit

if __name__ == "__main__":
    if platform.system() != "Windows":
        mp.set_start_method("forkserver")
    if platform.system() == "Darwin":
        info = AppKit.NSBundle.mainBundle().infoDictionary()
        info["LSBackgroundOnly"] = "1"
    from howdyCoder.start import start

    start()
