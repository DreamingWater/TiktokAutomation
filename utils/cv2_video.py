# Lenovo-"Xie Yan"


import cv2


def cv2_cut_first_frame(in_video_path, out_video_path):
    cap = cv2.VideoCapture(in_video_path)  # 打开视频文件
    ret, frame = cap.read()  # 从视频中读取第一帧
    if ret:  # 如果成功读取第一帧
        output_file_name = out_video_path  # 得输出文件路径
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 获得视频编解码器
        fps = int(cap.get(cv2.CAP_PROP_FPS))  # 获得视频帧率
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获得视频分辨率
        # 创建视频写入对象
        out = cv2.VideoWriter(output_file_name, fourcc, fps, (frame_width, frame_height))
        # 跳过第一帧
        ret, frame = cap.read()
        # 将帧写入输出视频文件
        while ret:
            out.write(frame)
            ret, frame = cap.read()
        # 释放资源
        cap.release()
        out.release()
        print("视频的第一帧已被删除并且输出到文件:", output_file_name)
    else:
        print("无法读取该视频文件%s" % in_video_path)
