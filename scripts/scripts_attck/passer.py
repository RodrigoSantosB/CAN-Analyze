import argparse
from attacks import CanAttack

parser = argparse.ArgumentParser(
                    prog='can attack',
                    description='can attack types',
                    epilog='Text at the bottom of help')


parser.add_argument('-f',  '--fuzzy', help='run the fuzzy ataque in can bus')
parser.add_argument('-d',  '--dos', help='run the dos ataque in can bus')
parser.add_argument('-m',  '--masquerate', help='run the masquerate ataque in can bus')
parser.add_argument('-m',  '--spoofed', help='run the spoofed ataque in can bus')


args = parser.parse_args()



