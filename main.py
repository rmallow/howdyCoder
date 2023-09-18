import multiprocessing as mp
import multiprocess as dill_mp
import platform

if __name__ == "__main__":
    if platform.system() != "Windows":
        mp.set_start_method("spawn")
        dill_mp.set_start_method("spawn")
    if platform.system() == "Darwin":
        pass
    from howdyCoder.start import start

    start()
