import os
import threading
import ffmpeg
import tempfile
import ImageSelector
import subprocess
import platform

def extract_frames(inputFiles:list[str], outputPath:str, terminationflag:threading.Event) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        ffmpegFiles = []
        for file in inputFiles:
            ffmpegFiles.append(ffmpeg.input(file))
            if terminationflag.is_set():
                return

        file_path = temp_dir + "tempconcatedfile.mp4"

        if terminationflag.is_set():
                return
        
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        if terminationflag.is_set():
                return

        ffmpeg.concat(*ffmpegFiles).output(filename=file_path).run()
        if terminationflag.is_set():
                return
        output_frame_path = os.path.join(outputPath, 'frame_%04d.jpeg')
        if terminationflag.is_set():
                return
        ffmpeg.input(filename=file_path).output(output_frame_path).run()

def filterImages(input_path, target_type:bool, target_count, terminationflag:threading.Event, groups:int = None, scalar:int = None) -> None:
    images = [os.path.join(input_path, img) for img in os.listdir(input_path) if img.lower().endswith(('.jpg','.jpeg','.png'))]
    images.sort()

    if terminationflag.is_set():
                return
    
    if target_type:
        print(len(images) * (target_count /100))
        print(int(len(images) * (target_count /100)))
        image_count = int(len(images) * (target_count /100))
    else:
        image_count = target_count
    selector = ImageSelector.ImageSelector(images)
    selected_images = selector.filter_sharpest_images(image_count, groups, scalar)
    
    if terminationflag.is_set():
                return
    
    for img in images:
            if terminationflag.is_set():
                return
                
            if img not in selected_images:
                os.remove(img)

def run_metashape(photos_path: str, metashape_name:str, metashape_output:str, colmap_output:str, **kwargs) -> None:
    script_args = ''
    if platform.system() == 'Linux':
        print("Sorry, linux support is not avalible at this time")
    elif platform.system() == 'Windows':
        try:
            metashape_path = kwargs['metashape_path']
        except:
            metashape_path = "C:\Program Files\Agisoft\Metashape Pro\metashape.exe"
        
        metashape_script_path = os.path.abspath("./metashape_script.py")        
            
        print("Fakerun " + str([metashape_path, "-r", metashape_script_path, "--name", metashape_name,"--metashape_output", metashape_output, "--output", colmap_output, "--input", photos_path]))
        #subprocess.run([meta_shape_path,  "-r", metashape_script_path] + script_args)
    else:
        print("Error, no supported OS detected for terminal commands")
        return

def backendFileProcessor(inputs:list[str], outputdir:str, retentionType:bool, retentionValue:int, terminationflag:threading.Event, groups:int | None = None, scalar:int | None = None, 
                        runMetashape:bool = False, metashape_name:str | None = None, metashape_output:str | None = None, colmap_output:str | None = None, metashape_path:str | None = None):
    extract_frames(inputs, outputdir, terminationflag)
    if terminationflag.is_set():
                return
    filterImages(outputdir,retentionType, retentionValue, terminationflag, groups, scalar)
    if terminationflag.is_set():
                return
    if runMetashape:
        arguments_to_pass = {}
        
        if metashape_path:
            arguments_to_pass['metashape_path'] = metashape_path

        run_metashape(photos_path=outputdir, metashape_name=metashape_name, metashape_output=metashape_output, colmap_output=colmap_output, kwargs=arguments_to_pass)

