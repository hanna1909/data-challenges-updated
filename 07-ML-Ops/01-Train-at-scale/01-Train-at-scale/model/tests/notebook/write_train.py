
from nbresult import ChallengeResult

from taxifare_model.interface.main import train

result = True
try:
    preprocess_and_train()
except:
    result = False

ChallengeResult(
    "train",
    result=result).write()
