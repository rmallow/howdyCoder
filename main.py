import multiprocessing as mp
import platform

if __name__ == "__main__":
    if platform.system() != "Windows":
        mp.set_start_method("forkserver")
    if platform.system() == "Darwin":
        pass
    from howdyCoder.start import start

    start()
