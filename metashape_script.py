import os
import Metashape
import argparse

def create_new_project() -> Metashape.app.document:
    doc = Metashape.app.document
    return doc

def get_chunk(doc:Metashape.app.document) -> Metashape.Chunk:
    chunk = doc.chunk
    return chunk

def add_photos_to_chunk(chunk:Metashape.Chunk, photo_paths:list[str]) -> None:
    chunk.addPhotos(photo_paths)

def align_photos(chunk:Metashape.Chunk) -> None:
    chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=False)
    chunk.alignCameras()

def export_cameras_to_colmap(chunk:Metashape.Chunk, path:str, filename:str) -> None:
    export_path = f"{path}/{filename}_COLMAP.txt"
    chunk.exportCameras(export_path, format=Metashape.CamerasFormatColmap)

def save_project(doc: Metashape.app.document, path:str=None, filename:str=None) -> None:
    if not(path and filename):
        doc.save()
    else:
        doc.save(path+"\\"+filename+".psx")

def display_metrics(chunk:Metashape.app.document.chunk, photocount, metashape_dir:str, project_name:str) -> None:
    aligned_count = 0
    for cam in chunk.cameras:
        if cam.transform is not None: # Check if camera has a valid transform matrix
            aligned_count += 1
    with open(metashape_dir+"\\"+project_name+'_point&photo_stats.txt', 'w') as file:
        file.write(f"Photos Alligned: {aligned_count}\\{photocount}\n")
        file.write(f"Total tie points: {len(chunk.tie_points.points)}")
        file.close()


def execute(export_path, project_name, images:list[str], metashape_dir:str) -> None:

    doc = create_new_project()
    chunk = get_chunk(doc)
    save_project(doc, metashape_dir, project_name)
    add_photos_to_chunk(chunk, images)
    save_project(doc)
    align_photos(chunk)
    save_project(doc)
    export_cameras_to_colmap(chunk, export_path, project_name)
    photocount = len(images)
    display_metrics(chunk, photocount, metashape_dir, project_name)
    save_project(doc)
    Metashape.app.quit()

if __name__ == '__main__':
    # Initialize the parser
    parser = argparse.ArgumentParser(description="A simple argument parser")

    # Add arguments
    parser.add_argument("-i", "--input") 
    parser.add_argument("-o", "--output") 
    parser.add_argument("-m", "--metashape_output") 
    parser.add_argument("-n", "--name")

    # Parse the arguments
    args = parser.parse_args()

    if not args.input:
        raise "Error, no input dir provided"
    elif not args.output:
        raise "Error, no ouput dir provided for the colmap data"
    elif not args.metashape_output:
        raise "Error, no output dir provided for the metashape file"
    elif not args.name:
        raise "Error, no output file naming convention"
    
    import_path = args.input
    export_path = args.output
    metashape_directory = args.metashape_output
    name = args.name
    entries = os.listdir(import_path)
    # Keep only files, not directories
    photos = []
    
    for file in entries:
        photos.append(str(import_path) + '\\' + str(file))

    execute(export_path, name, photos, metashape_directory)