import os
import scipy.io

# Function to load the triggers
def load_triggers(path,dmr):
    #prefixed = [filename for filename in os.listdir(path) if filename.startswith("AudiResp")]
    #path_triggers_dir= 'I:\Parooa\Synapse\i\kiloSorted_DMR\Triggers'
    #filename=find_triggers(path_triggers_dir,path)
    if os.path.exists(path):
        trig = scipy.io.loadmat(path)
        if dmr==1:
            return trig['TrigA'][0],path
        elif dmr==2:
            return trig['TrigB'][0],path
    else:
        print("Sorry, this folder doesn't exist, try another one")
        return
