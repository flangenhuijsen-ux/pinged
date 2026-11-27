#!/bin/bash
# render Shorts in look v2, one after another, two halves in parallel
for n in "$@"; do
  cd /home/claude/s$n || continue
  N=$(python3 src/lock_v2.py info | awk '{print $2}'); H=$((N/2))
  python3 src/lock_v2.py render 0 $H v2a > out/v2a.log 2>&1 &
  python3 src/lock_v2.py render $H $N v2b > out/v2b.log 2>&1 &
  wait
  printf "file v2a.mp4\nfile v2b.mp4\n" > out/c2.txt
  ffmpeg -v error -y -f concat -i out/c2.txt -c copy out/v2.mp4 && ffmpeg -v error -y -i out/v2.mp4 -i out/mix3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/v2_full.tmp.mp4 && mv out/v2_full.tmp.mp4 out/v2_full.mp4 && python3 /home/claude/outro/outro_v2.py out/v2_full.mp4 out/v2_final.mp4 && echo "s$n ok (met slot)" >> /home/claude/gen/render_v2.log
done

