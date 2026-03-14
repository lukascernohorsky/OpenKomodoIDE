#!/bin/bash
update_progress() {
    local step_name=$1
    local status=$2
    local timestamp=$(date +%Y-%m-%d\ %H:%M:%S)
    local PROGRES_FILE="/home/lc/projekty/OpenKomodoIDE/PROGRES.md"
    
    sed -i "s/- \[ \] $step_name/- \[$status\] $step_name/" "$PROGRES_FILE"
    sed -i "s/^## Current State$/## Current State\n- **Last Completed Step**: $step_name\n- **Status**: $status\n- **Timestamp**: $timestamp/" "$PROGRES_FILE"
    echo "[$timestamp] $step_name: $status" >> "$PROGRES_FILE"
}

handle_interruption() {
    local step_name=$1
    echo "Build interrupted during: $step_name"
    update_progress "$step_name" "interrupted"
    touch "/home/lc/projekty/OpenKomodoIDE/BUILD_INTERRUPTED"
}
