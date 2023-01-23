import logging

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.ERROR)

logger = logging.getLogger(__name__)

ALPHABET = "~!@#$$%^&*()_+`1234567890-=[]\\{}|:\";',./<>?qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"


def cat_side(asciiart, gap=4):
    counts = []
    max_widths = []
    ascall = ""
    missing_char = "!"
    for i, asc in enumerate(asciiart):
        logger.debug([i, asc])
        lines = asc.splitlines()
        counts.append(len(lines))
        try:
            mwd = max([len(l) for l in lines])
        except ValueError as e:
            mwd = 0
        max_widths.append(mwd)
        ascall += asc
    for c in ALPHABET:
        if c not in ascall:
            missing_char = c
            break
    logger.debug(counts)
    maxl = max(counts) + 1
    for i, c in enumerate(counts):
        st = c * missing_char
        # https://stackoverflow.com/a/5676884
        # https://peps.python.org/pep-0498/
        # use > < ^ for alignment https://docs.python.org/2/library/string.html#format-specification-mini-language
        asciiart[i] = format(st, f"\n^{maxl}").replace(st, asciiart[i])
    res = ""
    # https://stackoverflow.com/a/59211229
    for lines in zip(*map(str.splitlines, asciiart)):
        res += "".join(line.ljust(min(max_widths) + gap) for line in lines) + "\n"
    return res


def cat_down(asciiart):
    # TODO algin logic just str concat for now
    ret = ""
    for asc in asciiart:
        ret += asc
    return ret


def cat_grid(asciiart, gridfmt):
    import re

    ds = re.compile(r"\{\d+\}")
    dat = []
    p = [""] + asciiart
    logger.debug(len(p))
    for l in gridfmt.splitlines():
        if l == "":
            continue
        sides = []
        for x in ds.findall(l):
            sides.append(x.format(*p))
        logger.debug([l, sides])
        if sides:
            dat.append(cat_side(sides))
    return cat_down(dat)


def place_ascii(asciiart, placement="side", gridfmt=None):
    # placement can be side, down, grid
    # eg:
    # -  {1}{2}...
    # -   {1}
    #     {2}
    #     ...
    # - {1}{2}
    #   {3}{4}
    # - Use {0} for empty space, eg. try with {1}{0}{2}
    if placement == "side":
        return cat_side(asciiart)
    elif placement == "down":
        return cat_down(asciiart)
    elif placement == "grid":
        return cat_grid(asciiart, gridfmt)
    else:
        logger.error(f"wrong placement type `{placement}` only side,down,grid allowed")
        return


def cat_files(files, placement):
    asccs = []
    for i, fi in enumerate(files):
        with open(fi, "r", encoding="utf8") as ff:
            content = ff.read()
            appent = f'{content}\n    {".".join(fi.split("/")[-1].split(".")[:-1])}\n'
            # appent = f'{content}\nfile:{fi}\n'
            # appent = content
            if placement == "grid" and i == 0:
                appent = content
            asccs.append(appent)
    if placement == "grid":
        return place_ascii(asccs[1:], placement, asccs[0])
    return place_ascii(asccs, placement)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        logger.error(f"Usage:\tpython {sys.argv[0]} <placement> <files...>")
        logger.error("\tplacement:\t[side|down|grid]")
        logger.error("\tnote:\t\tif placement is grid first file is the grid format")
        exit(1)

    print(cat_files(sys.argv[2:], sys.argv[1]))
