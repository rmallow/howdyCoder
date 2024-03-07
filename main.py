import multiprocessing as mp
import platform

if __name__ == "__main__":
    if platform.system() != "Windows":
        mp.set_start_method("spawn")
    if platform.system() == "Darwin":
        pass
    from howdyCoder.start import start

    start()
