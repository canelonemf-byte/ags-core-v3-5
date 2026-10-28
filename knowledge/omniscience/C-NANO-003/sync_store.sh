#!/bin/bash
D=/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-NANO-003; mkdir -p $D
cd /workspace/omniscience_cnano003 && cp -r code out logs smoke prereg_C-NANO-003.md prereg_C-NANO-003.FROZEN.md prereg_C-NANO-003.sha256 code_freeze.sha256 freeze_stamp.txt desviaciones.md run_all.sh sync_store.sh $D/ 2>/dev/null; [ -f results.json ] && cp results.json $D/; [ -f eval.log ] && cp eval.log $D/; rm -f $D/out/gpaw/vib*.json 2>/dev/null; true
