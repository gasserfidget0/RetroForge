import win32api
import win32file

def get_removable_drives():
    drives = []
    try:
        drive_strings = win32api.GetLogicalDriveStrings()
        drive_letters = [d for d in drive_strings.split('\x00') if d]
        
        for drive in drive_letters:
            try:
                drive_type = win32file.GetDriveType(drive)
                # 2 is DRIVE_REMOVABLE
                if drive_type == win32file.DRIVE_REMOVABLE:
                    try:
                        vol_info = win32api.GetVolumeInformation(drive)
                        vol_name = vol_info[0] if vol_info[0] else "Removable Drive"
                        fs_name = vol_info[4]
                    except:
                        vol_name = "Unknown"
                        fs_name = "Unknown"
                        
                    try:
                        space_info = win32api.GetDiskFreeSpaceEx(drive)
                        total_bytes = space_info[1]
                        free_bytes = space_info[0]
                        total_gb = round(total_bytes / (1024**3), 2)
                        free_gb = round(free_bytes / (1024**3), 2)
                    except:
                        total_gb = 0
                        free_gb = 0
                        
                    drives.append({
                        "letter": drive[:2],
                        "name": vol_name,
                        "file_system": fs_name,
                        "total_gb": total_gb,
                        "free_gb": free_gb,
                        "description": f"{drive[:2]} [{vol_name}] - {total_gb} GB"
                    })
            except Exception:
                continue
    except Exception as e:
        print(f"Error enumerating drives: {e}")
        
    return drives
