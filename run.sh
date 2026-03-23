rm -rf particles_frames.txt va_vs_time.png
cd java
javac *.java
#java App <N> <L> <M> <rc> <periodic> <iterations> <eta> <leaderID> <circleLeader>
java App 100 10 5 1 true 500 0.0 0 true
cd ..
if [ "$1" == "T" ]; then
    rm -rf output.gif
    python3 vis_thom.py
else
    python3 visualize.py
fi
python3 plot_va.py