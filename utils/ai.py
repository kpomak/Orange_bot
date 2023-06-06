import os

from bardapi import Bard

token = os.getenv("BARD_API_KEY")
bard = Bard(token=token)
