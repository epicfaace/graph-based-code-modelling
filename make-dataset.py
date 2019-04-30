import os
import shutil

## In the actual paper they used ravendb as a dev project but it had a GPL license and wasn't released
DEV_PROJECTS = ['commonmark', 'rxnet'] 
TEST_PROJECTS = ['commandline', 'humanizer', 'lean']
DATASET_PATH = 'graph-dataset'

OUTPUT_FOLDER = os.path.join(DATASET_PATH, 'reorganized')

def copy_and_rename_dir(src_dir, dst_dir, copy = False):
    for filename in os.listdir(src_dir):
        new_filename = filename
        if '.json.gz' not in filename:
            new_filename = filename.replace('.gz', '.json.gz')
        print('src:', os.path.join(src_dir, filename))
        print('dst:', os.path.join(dst_dir, new_filename))
        if copy:
            shutil.copyfile(os.path.join(src_dir, filename), os.path.join(dst_dir, new_filename))

def parse_dir(entry, copy = False):
    print()
    print(entry.name)
    if entry.name in DEV_PROJECTS:
        src_dir = os.path.join(entry.path, 'graphs')
        dst_dir = os.path.join(OUTPUT_FOLDER, 'graphs-valid')
        copy_and_rename_dir(src_dir, dst_dir, copy)
    elif entry.name in TEST_PROJECTS:
        src_dir = os.path.join(entry.path, 'graphs')
        dst_dir = os.path.join(OUTPUT_FOLDER, 'graphs-test/unseen')
        copy_and_rename_dir(src_dir, dst_dir, copy)
    else:
        ## look at train/dev/test + move type lattice
        graphs_train = os.path.join(entry.path, 'graphs-train')
        graphs_valid = os.path.join(entry.path, 'graphs-valid')
        graphs_test = os.path.join(entry.path, 'graphs-test')
        
        train_dst = os.path.join(OUTPUT_FOLDER, 'graphs-train')
        valid_dst = os.path.join(OUTPUT_FOLDER, 'graphs-valid')
        test_dst = os.path.join(OUTPUT_FOLDER, 'graphs-test/seen')

        copy_and_rename_dir(graphs_train, train_dst, copy)
        copy_and_rename_dir(graphs_valid, valid_dst, copy)
        copy_and_rename_dir(graphs_test, test_dst, copy)

        hierarchy_file = entry.name + '-typehierarchy.json.gz'
        src = os.path.join(entry.path, hierarchy_file)
        dst = os.path.join(OUTPUT_FOLDER, 'type-hierarchies', hierarchy_file)
        print('src:', src)
        print('dst:', dst)
    print()


if __name__ == "__main__":
    # os.makedir(OUTPUT_FOLDER)
    # os.makedir(os.path.join(OUTPUT_FOLDER, 'graphs-train'))
    # os.makedir(os.path.join(OUTPUT_FOLDER, 'graphs-test'))
    # os.makedir(os.path.join(OUTPUT_FOLDER, 'graphs-test/seen'))
    # os.makedir(os.path.join(OUTPUT_FOLDER, 'graphs-test/unseen'))
    # os.makedir(os.path.join(OUTPUT_FOLDER, 'graphs-valid'))
    # os.makedir(os.path.join(OUTPUT_FOLDER, 'type-hierarchies'))
    for entry in os.scandir(DATASET_PATH):
        if entry.is_dir():
            parse_dir(entry)