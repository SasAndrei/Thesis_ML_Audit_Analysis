PANDAS = False
DATASET = []
HEADS = []
MISSING = 0
SPLIT = ["train_test_split", "KFold"]
EVAL = ["confusion_matrix", "accuracy_score", "precision_score", "recall_score", "f1_score", "precision_recall_curve", "roc_curve"]
MODELS = {}
MODE = "Developer"


def reset_globals():
    global PANDAS
    global DATASET
    global HEADS
    global MISSING
    global MODELS
    PANDAS = False
    DATASET = []
    HEADS = []
    MISSING = 0
    MODELS = []


def mode(m):
    global MODE
    MODE = m
