import scipy.io as sio
import os
import json


def make_summe():
    print("Setting configurations...")
    CURR_DIR = os.getcwd()
    DATA_DIR = CURR_DIR + '/../data/SumMe/GT/'
    keys_to_remove = ['__globals__', '__header__', '__version__', 'all_userIDs']

    print("Reading data from SumMe Matlab files...")
    data = {}
    for document in os.listdir(DATA_DIR):
        path = DATA_DIR + document
        d = {key: value for key, value in sio.loadmat(path).items()
             if key not in keys_to_remove}
        d['FPS'] = str(d['FPS'][0][0])
        d['nFrames'] = str(d['nFrames'][0][0])
        d['video_duration'] = str(d['video_duration'][0][0])
        d['gt_score'] = [str(v[0]) for v in d['gt_score']]
        d['user_score'] = [list(v) for v in d['user_score']]
        user_scores = []
        for scores in d['user_score']:
            user_scores.append(map(str, scores))
        d['user_score'] = user_scores
        d['segments'] = [list(v) for v in d['segments'][0]]
        segments = []
        for sets in d['segments']:
            values = []
            for v in sets:
                values.append(map(str, list(v)))
            segments.append(list(map(list, values)))
        d['segments'] = segments
        data[document.split('.')[0]] = d

    print("Saving JSON dataset format in '../dataset/summe_dataset.json'...")
    with open('../dataset/summe_dataset.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    make_summe()
