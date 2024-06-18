import tensorflow as tf
from move_prediction.maia_chess_backend.maia.net import Net
import numpy as np


if __name__ == "__main__":
    model = Net()
    model.parse_proto(r"C:\Users\magle\Desktop\Dateien\Python\maia-chess\maia_weights\maia-1900.pb.gz")
    print([print(len(a)) for a in model.get_weights()])