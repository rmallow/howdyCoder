import multiprocessing as mp
import platform

if __name__ == "__main__":
    if platform.system() != "Windows":
        mp.set_start_method("forkserver")
    from algoBuilder.start import start

    start()
