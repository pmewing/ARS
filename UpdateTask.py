class Update:
    def __init__(self, program, current, total):
        print("\r{program} has started file {current} / {total}".format(
            program=program,
            current=current,
            total=total)
        )
