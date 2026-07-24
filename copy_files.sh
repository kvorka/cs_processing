#!/bin/bash
copy_data() {
    if [ ! -d "$2" ]; then
        mkdir -p "$2"
    fi
    
    cp "$1"monitor.0000000000.t* "$2" &
    cp "$1"state.0000000000.t* "$2" &
    cp "$1"grid.t* "$2" &
    
    wait
}

copy_data "/nfsjk/kvorka/MITgcm-tides-custom-latest/run-flat/" "state/flat_64x64x50_Ah=10_Av=1/"
#copy_data "/nfsjk/kvorka/MITgcm-tides-custom-latest/run-flat/" "state/flat_64x64x50_Ah=10_Av=10/"
#copy_data "/nfsjk/kvorka/MITgcm-tides-custom-latest/run-ridge/" "state/ridge10_64x64x50_Ah=10_Av=10/"