# archivos.py
import os
import uuid
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    """Verificar si la extensión del archivo está permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def guardar_archivo(file, upload_folder, allowed_extensions):
    """Guardar un archivo en el servidor"""
    if file and allowed_file(file.filename, allowed_extensions):
        # Generar nombre único para el archivo
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        
        # Guardar archivo
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        return unique_filename, original_filename
    return None, None

def eliminar_archivo(filename, upload_folder):
    """Eliminar un archivo del servidor"""
    if filename:
        file_path = os.path.join(upload_folder, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except:
                return False
    return False