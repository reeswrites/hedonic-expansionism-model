#!/usr/bin/env bash
# Regenerate every saved result in results/. Run from the repo root.
set -e
cd "$(dirname "$0")/model"
OUT=../results
run() { echo "== $1 $2"; python3 "$1" $2 > "$OUT/${1%.py}${3}.txt"; }
run hx_model.py
run hx_model_v1.py
run hx_v1_variant.py
run hx_v1_wall.py
run hx_v1_middle.py "combo" ""
run hx_v1_middle.py "combo wall" "_wall"
run hx_model_v2.py
run hx_v2_symmetric.py
run hx_p4.py "" "_out"
run hx_relief_types.py
run hx_relief_types2.py
run hx_pleasure_relief.py
run hx_pleasure_relief_phased.py
run hx_p7.py
run hx_updates.py "" "_out"
run hx_social.py
run hx_social_vs_solo.py
run hx_alone_vs_social.py
run hx_broad_social_vs_solo.py
run hx_yield_reference.py
run hx_adaptation_ladder.py
run hx_arousal.py
run hx_lifespan.py
run hx_meaning.py
run hx_death.py
run hx_combined.py
run hx_craving.py
run hx_assumption_checks.py
run hx_pair.py
run hx_acquired_taste.py
echo done
