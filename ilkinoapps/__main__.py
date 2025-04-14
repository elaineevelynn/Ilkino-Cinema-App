from ilkinoapps.ilkino import *
import sys

if __name__ == "__main__":
    # INPUT USING COMMAND PROMPT
    # python -m ilkinoapps --gift=pack_of_candy,key_hanger,teddy_bear,chocolate,cute_pencil
    tmp = sys.argv[1:]
    gift_input = tmp[0]
    ls_gifts = list(gift_input[7:].split(","))

    ilkino = Ilkino(RealGenerator.generate(), RealPrinter())
    ilkino.setup(ls_gifts)
    ilkino.run()
