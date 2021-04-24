'''
  create bat file to copy all importent files from 
  the user home folder to a backup

'''


import os
from os.path import join
from pathlib import Path
import logging
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('dest', 'c:\\backup', 'destination folder')
backup_files_type= ['.doc','.docx','.jpeg','.jpg','.png','.gif','.tiff','.pdf','.xls','.xlsx','.avi']
backup_folders_name= ['Documets','Downloads','Pictures']
bat_filename='supercopy.bat.txt'
copy_command='robocopy'
copy_command_flags='/CREATE /B'

def scan_folder_level1(src_folder,dest_folder):
  fid=open(bat_filename,'w',encoding="utf-8")
  for p in Path(src_folder).glob('**/*'):
    if p.is_file() and p.suffix in backup_files_type:
      d=dest_folder / p.parts[-2] 
      fid.write(f'{copy_command} "{p}" "{d}" {copy_command_flags} \n')
      #print(p.name)
      #breakpoint()
  fid.close() 

def main(argv):
  if not os.environ['os']== 'Windows_NT':
    logging.error('run on windows on only')
    return

  src_folder=join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'])
  
  user_name=os.environ['USERNAME']
  dest_folder=join(FLAGS.dest,os.environ['COMPUTERNAME'],user_name)
  for subf in backup_folders_name:
    f=Path(src_folder) / Path(subf)
    d=Path(dest_folder) / Path(subf)
    logging.info(f'copy from: {f} to: {dest_folder}')
    scan_folder_level1(f,d)

if __name__ == '__main__':
  app.run(main)

