import os
import shutil

#source_dir = "pdf_inbox"
#target_dir = "pdf_examples"


def sys_log_entry(routine, log_value):
    ''' 
    Inserts data into a postgres table for the purposes of logging 
    automation system activities.
    '''
    # NOTE: table automatically adds a timestamp on entry
    # insert_time, routine, log_value
    print(routine, log_value)


def move_file(current_dir, target_dir, file_name):
        '''
        Move pdf file to another directory
        '''
        #shutil.copy2(os.path.join(current_dir, file_name), target_dir)
        shutil.move(os.path.join(current_dir, file_name), target_dir)


def to_working_dir(source_dir, target_dir):
    
    n_files_source = len(os.listdir(source_dir))

    try:
        if n_files_source > 0:   # are there files?
            for file_name in os.listdir(source_dir):   # move files from source to target
                move_file(source_dir, target_dir, file_name)

            n_files_target = len(os.listdir(target_dir))
            if n_files_target == n_files_source:
                log_value = f"Files in inbox: {n_files_source}. Moved to working dir: {n_files_target}. "
                sys_log_entry("move", log_value)
                return True
        
        else:  # when there are no files in the inbox
            # make log entry
            sys_log_entry("no files", f"There are no files in the {source_dir} directory.")
            return False
            
    except:
        # error moving files.
        error_msg = "There was an error accessing or moving the PDF files."
        sys_log_entry("error", "error_msg")
        print(error_msg)
        return False
    
