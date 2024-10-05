# import cv2
# import torch
# import numpy as np
# from scipy.spatial import distance
# from model import BallTrackerNet
# from general import postprocess
# from tqdm import tqdm
# from itertools import groupby
#
# def preprocess_frame(frame, prev_frame, prev_prev_frame, height=360, width=640):
#     """
#     Preprocess three consecutive frames for model input.
#     """
#     frame = cv2.resize(frame, (width, height))
#     prev_frame = cv2.resize(prev_frame, (width, height))
#     prev_prev_frame = cv2.resize(prev_prev_frame, (width, height))
#
#     imgs = np.concatenate((frame, prev_frame, prev_prev_frame), axis=2)
#     imgs = imgs.astype(np.float32) / 255.0
#     imgs = np.rollaxis(imgs, 2, 0)
#
#     inp = np.expand_dims(imgs, axis=0)
#     return inp
#
# def infer_pytorch_model(model, inp, device, original_height, original_width):
#     """
#     Run PyTorch model inference.
#     """
#     inp = torch.from_numpy(inp).float().to(device)
#     with torch.no_grad():
#         out = model(inp)
#     output = out.argmax(dim=1).detach().cpu().numpy()
#
#     x_pred, y_pred = postprocess(output)
#
#     if x_pred is not None and y_pred is not None:
#         x_pred = int(x_pred * original_width / 640)
#         y_pred = int(y_pred * original_height / 360)
#
#     return x_pred, y_pred
#
# def remove_outliers(ball_track, dists, max_dist=100):
#     """
#     Remove outliers from model prediction.
#     """
#     outliers = list(np.where(np.array(dists) > max_dist)[0])
#     for i in outliers:
#         if (dists[i+1] > max_dist) | (dists[i+1] == -1):
#             ball_track[i] = (None, None)
#             outliers.remove(i)
#         elif dists[i-1] == -1:
#             ball_track[i-1] = (None, None)
#     return ball_track
#
# def split_track(ball_track, max_gap=4, max_dist_gap=80, min_track=5):
#     """
#     Split ball track into several subtracks for interpolation.
#     """
#     list_det = [0 if x[0] else 1 for x in ball_track]
#     groups = [(k, sum(1 for _ in g)) for k, g in groupby(list_det)]
#
#     cursor = 0
#     min_value = 0
#     result = []
#     for i, (k, l) in enumerate(groups):
#         if (k == 1) & (i > 0) & (i < len(groups) - 1):
#             dist = distance.euclidean(ball_track[cursor-1], ball_track[cursor+l])
#             if (l >= max_gap) | (dist/l > max_dist_gap):
#                 if cursor - min_value > min_track:
#                     result.append([min_value, cursor])
#                     min_value = cursor + l - 1
#         cursor += l
#     if len(list_det) - min_value > min_track:
#         result.append([min_value, len(list_det)])
#     return result
#
# def interpolation(coords):
#     """
#     Run ball interpolation in one subtrack.
#     """
#     def nan_helper(y):
#         return np.isnan(y), lambda z: z.nonzero()[0]
#
#     x = np.array([x[0] if x[0] is not None else np.nan for x in coords])
#     y = np.array([x[1] if x[1] is not None else np.nan for x in coords])
#
#     nons, yy = nan_helper(x)
#     x[nons] = np.interp(yy(nons), yy(~nons), x[~nons])
#     nans, xx = nan_helper(y)
#     y[nans] = np.interp(xx(nans), xx(~nans), y[~nans])
#
#     track = [*zip(x,y)]
#     return track
#
# def draw_ball_on_frame(frame, ball_track, trace=7):
#     """
#     Draw ball coordinates and trace on the frame.
#     """
#     for i in range(trace):
#         if len(ball_track) > i and ball_track[-i-1][0]:
#             x, y = ball_track[-i-1]
#             frame = cv2.circle(frame, (int(x), int(y)), radius=0, color=(0, 0, 255), thickness=10-i)
#     return frame
#
# def real_time_inference(model, device, video_source=0):
#     """
#     Perform real-time inference on video using PyTorch model.
#     """
#     cap = cv2.VideoCapture(video_source)
#     ret, frame = cap.read()
#
#     if not ret:
#         print("Error: Unable to read video feed.")
#         return
#
#     prev_frame = frame
#     prev_prev_frame = frame
#
#     original_height, original_width = frame.shape[:2]
#
#     ball_track = []
#     dists = []
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         inp = preprocess_frame(frame, prev_frame, prev_prev_frame)
#         x_pred, y_pred = infer_pytorch_model(model, inp, device, original_height, original_width)
#
#         ball_track.append((x_pred, y_pred))
#
#         if len(ball_track) > 1 and ball_track[-1][0] and ball_track[-2][0]:
#             dist = distance.euclidean(ball_track[-1], ball_track[-2])
#         else:
#             dist = -1
#         dists.append(dist)
#
#         if len(ball_track) > 50:  # Process in batches
#             ball_track = remove_outliers(ball_track, dists)
#             subtracks = split_track(ball_track)
#             for r in subtracks:
#                 ball_subtrack = ball_track[r[0]:r[1]]
#                 ball_subtrack = interpolation(ball_subtrack)
#                 ball_track[r[0]:r[1]] = ball_subtrack
#
#             frame_with_ball = draw_ball_on_frame(frame, ball_track)
#             cv2.imshow('Real-Time Ball Tracking', frame_with_ball)
#
#             ball_track = ball_track[-30:]  # Keep only recent tracks
#             dists = dists[-30:]
#
#         prev_prev_frame = prev_frame
#         prev_frame = frame
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
# if __name__ == '__main__':
#     model_path = 'model_best.pt'
#     model = BallTrackerNet()
#     model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
#     model.eval()
#
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = model.to(device)
#
#     real_time_inference(model, device, video_source="input_video3.mp4")



import cv2
import torch
import numpy as np
from scipy.spatial import distance
from model import BallTrackerNet
from general import postprocess
from tqdm import tqdm
from itertools import groupby

def preprocess_frame(frame, prev_frame, prev_prev_frame, height=360, width=640):
    """
    Preprocess three consecutive frames for model input.
    """
    frame = cv2.resize(frame, (width, height))
    prev_frame = cv2.resize(prev_frame, (width, height))
    prev_prev_frame = cv2.resize(prev_prev_frame, (width, height))

    imgs = np.concatenate((frame, prev_frame, prev_prev_frame), axis=2)
    imgs = imgs.astype(np.float32) / 255.0
    imgs = np.rollaxis(imgs, 2, 0)

    inp = np.expand_dims(imgs, axis=0)
    return inp

def infer_pytorch_model(model, inp, device, original_height, original_width):
    """
    Run PyTorch model inference.
    """
    inp = torch.from_numpy(inp).float().to(device)
    with torch.no_grad():
        out = model(inp)
    output = out.argmax(dim=1).detach().cpu().numpy()

    x_pred, y_pred = postprocess(output)

    if x_pred is not None and y_pred is not None:
        x_pred = int(x_pred * original_width / 640)
        y_pred = int(y_pred * original_height / 360)

    return x_pred, y_pred

def remove_outliers(ball_track, dists, max_dist=100):
    """
    Remove outliers from model prediction.
    """
    outliers = list(np.where(np.array(dists) > max_dist)[0])
    for i in outliers:
        if (dists[i+1] > max_dist) | (dists[i+1] == -1):
            ball_track[i] = (None, None)
            outliers.remove(i)
        elif dists[i-1] == -1:
            ball_track[i-1] = (None, None)
    return ball_track

def split_track(ball_track, max_gap=4, max_dist_gap=80, min_track=5):
    """
    Split ball track into several subtracks for interpolation.
    """
    list_det = [0 if x[0] else 1 for x in ball_track]
    groups = [(k, sum(1 for _ in g)) for k, g in groupby(list_det)]

    cursor = 0
    min_value = 0
    result = []
    for i, (k, l) in enumerate(groups):
        if (k == 1) & (i > 0) & (i < len(groups) - 1):
            dist = distance.euclidean(ball_track[cursor-1], ball_track[cursor+l])
            if (l >= max_gap) | (dist/l > max_dist_gap):
                if cursor - min_value > min_track:
                    result.append([min_value, cursor])
                    min_value = cursor + l - 1
        cursor += l
    if len(list_det) - min_value > min_track:
        result.append([min_value, len(list_det)])
    return result

def interpolation(coords):
    """
    Run ball interpolation in one subtrack.
    """
    def nan_helper(y):
        return np.isnan(y), lambda z: z.nonzero()[0]

    x = np.array([x[0] if x[0] is not None else np.nan for x in coords])
    y = np.array([x[1] if x[1] is not None else np.nan for x in coords])

    nons, yy = nan_helper(x)
    x[nons] = np.interp(yy(nons), yy(~nons), x[~nons])
    nans, xx = nan_helper(y)
    y[nans] = np.interp(xx(nans), xx(~nans), y[~nans])

    track = [*zip(x,y)]
    return track

def draw_ball_on_frame(frame, ball_track, trace=7):
    """
    Draw ball coordinates and trace on the frame.
    """
    for i in range(trace):
        if len(ball_track) > i and ball_track[-i-1][0]:
            x, y = ball_track[-i-1]
            frame = cv2.circle(frame, (int(x), int(y)), radius=0, color=(0, 0, 255), thickness=10-i)
    return frame

def real_time_inference(model, device, video_source=0):
    """
    Perform real-time inference on video using PyTorch model.
    """
    cap = cv2.VideoCapture(video_source)
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to read video feed.")
        return

    prev_frame = frame
    prev_prev_frame = frame

    original_height, original_width = frame.shape[:2]

    ball_track = []
    dists = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        inp = preprocess_frame(frame, prev_frame, prev_prev_frame)
        x_pred, y_pred = infer_pytorch_model(model, inp, device, original_height, original_width)

        ball_track.append((x_pred, y_pred))

        if len(ball_track) > 1 and ball_track[-1][0] and ball_track[-2][0]:
            dist = distance.euclidean(ball_track[-1], ball_track[-2])
        else:
            dist = -1
        dists.append(dist)

        if len(ball_track) > 50:  # Process in batches
            ball_track = remove_outliers(ball_track, dists)
            subtracks = split_track(ball_track)
            for r in subtracks:
                ball_subtrack = ball_track[r[0]:r[1]]
                ball_subtrack = interpolation(ball_subtrack)
                ball_track[r[0]:r[1]] = ball_subtrack

            frame_with_ball = draw_ball_on_frame(frame, ball_track)
            cv2.imshow('Real-Time Ball Tracking', frame_with_ball)

            ball_track = ball_track[-30:]  # Keep only recent tracks
            dists = dists[-30:]

        prev_prev_frame = prev_frame
        prev_frame = frame

        # Check if 'q' is pressed and break loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close windows after 'q' press
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    model_path = 'model_best.pt'
    model = BallTrackerNet()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    real_time_inference(model, device, video_source="input_video3.mp4")
