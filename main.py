import multiprocessing as mp

if __name__ == "__main__":
    # mp.freeze_support()
    mp.set_start_method("forkserver")
    from algoBuilder.start import start

    start()
