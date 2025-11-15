import os
import ffmpeg
import tempfile
import ImageSelector

def extract_frames(inputFiles:list[str], outputPath:str):
    with tempfile.TemporaryDirectory() as temp_dir:
        ffmpegFiles = []
        for file in inputFiles:
            ffmpegFiles.append(ffmpeg.input(file))

        file_path = temp_dir + "tempconcatedfile.mp4"

        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        ffmpeg.concat(*ffmpegFiles).output(filename=file_path).run()
        output_frame_path = os.path.join(outputPath, 'frame_%04d.jpeg')
        ffmpeg.input(filename=file_path).output(output_frame_path).run()

def filterImages(input_path, target_type:bool, target_count, groups = None, scalar = None):
    images = [os.path.join(input_path, img) for img in os.listdir(input_path) if img.lower().endswith(('.jpg','.jpeg','.png'))]
    images.sort()
    print(images)
    
    if target_type:
        print(len(images) * (target_count /100))
        print(int(len(images) * (target_count /100)))
        image_count = int(len(images) * (target_count /100))
    else:
        image_count = target_count
    selector = ImageSelector.ImageSelector(images)
    selected_images = selector.filter_sharpest_images(image_count, groups, scalar)
    
    for img in images:
            if img not in selected_images:
                os.remove(img)