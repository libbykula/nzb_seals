import os 
import pandas as pd

user_dir = 'C:/Users/kibby'
extra_dirs = ['Files', 'seals', 'projects']
project_name = 'spain_30m'
project_dir = os.path.join(user_dir, os.sep.join(extra_dirs), project_name)


block_list_dir = os.path.join(project_dir, 'intermediate/allocations/ssp1/rcp26/seals/bau/2050/allocation_zones')

block_list = pd.read_csv(os.path.join(block_list_dir, 'global_processing_blocks_list.csv'))

block_list_all = list(block_list.iloc[:, 0].astype(str) + '_' + block_list.iloc[:, 1].astype(str))

block_list_done = [f for f in os.listdir(block_list_dir) if os.path.isdir(os.path.join(block_list_dir, f))]

block_list_broken = [f for f in block_list_all if f not in block_list_done]

# print(block_list_broken)